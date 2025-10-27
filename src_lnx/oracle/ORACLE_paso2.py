# ----------------------------------------------------------------------------------------
#  PASO2: Validar Datos Locales vs Oracle, comprobamos que no estén en producción los 
#         nuevos registros a anexar.
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.ORACLE_variables as sTv
from   cfg.ORACLE_librerias import *
from   cfg.ORACLE_conection import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

# Valida si existe una tabla en concreto en oracle
def existe_tabla(cursor, nombre_tabla):
    query = f"""
    SELECT table_name FROM user_tables 
    WHERE table_name = UPPER('{nombre_tabla}')
    """
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado is not None
  
# Comprueba si el resgistro del dataframe"row" existe en la bbbdd de eventos relevantes
def existe_en_oracle(cursor, row):
    """
    Comprueba si existe el registro 'row' en la tabla P_BOLSAS_EVENTOS_RELEVANTES.
    Usa binds nombrados compatibles con oracledb.
    """
    from datetime import datetime as dt
    try:
        import pandas as _pd
        has_pandas = True
    except Exception:
        has_pandas = False

    where_clauses = []
    params = {}

    # Campos fijos
    fixed_cols = ['FECHA', 'N', 'CLAVE', 'SECCION', 'ASUNTO', 'URL']
    for col in fixed_cols:
        where_clauses.append(f"{col} = :{col}")
        val = row[col]
        # Si es pandas.Timestamp, convertir a python datetime
        if has_pandas and hasattr(val, "to_pydatetime"):
            val = val.to_pydatetime()
        params[col] = val

    # ARCHIVO: si es NULL usar "IS NULL", si no usar bind
    archivo = row.get('ARCHIVO', None)
    is_null = False
    if has_pandas:
        is_null = _pd.isna(archivo)
    else:
        is_null = (archivo is None)
    if is_null:
        where_clauses.append("ARCHIVO IS NULL")
    else:
        where_clauses.append("ARCHIVO = :ARCHIVO")
        params['ARCHIVO'] = archivo

    # Campos finales
    for col in ['ORIGEN', 'T', 'FILTRO']:
        where_clauses.append(f"{col} = :{col}")
        params[col] = row[col]

    sql = "SELECT 1 FROM P_BOLSAS_EVENTOS_RELEVANTES WHERE " + " AND ".join(where_clauses)

    try:
        # DEBUG: descomenta si quieres ver SQL y params en cada ejecución
        # print("SQL:", sql)
        # print("Params:", params)
        cursor.execute(sql, params)
        return cursor.fetchone() is not None
    except Exception as e:
        # Mostrar información útil para depurar
        print(Fore.RED + f"{dt.now().time()} - Error en existe_en_oracle: {e}")
        print("SQL:", sql)
        print("Params:", params)
        raise
        
# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2(var_Fechas3):

    if len(sTv.df_Global) == 0:
        print(Fore.RED + "No hay datos en el DataFrame, probar a ejecutar el paso1")
    else:
        print(f"OK: Existen {len(sTv.df_Global)} registros en el DataFrame para analizar")

        # Oracle, Parámetros de conexión:
        oracle_dns=sTv.var_Ora_DNS
        oracle_uid=sTv.var_Ora_UID
        oracle_pwd=sTv.var_Ora_PWD

        # Oracle, Establecer Conexión Oracle:
        conexion, cursor=Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

        # Validamos si existe o no una tabla Oracle    
        if cursor:
            if existe_tabla(cursor, sTv.var_Ora_TAB1):
                print(f"OK: La tabla de ORACLE {sTv.var_Ora_TAB1} Existe.")
            else:
                print(Fore.RED + f"La tabla {sTv.var_Ora_TAB1} NO existe.")
                sys.exit(0)

        # Validar duplicados
        for idx, row in sTv.df_Global.iterrows():
            if existe_en_oracle(cursor, row):
                rutaEntrada=f'{sTv.var_RutaIN}{sTv.var_Files_IN}_{var_Fechas3}.xlsx'
                print(Fore.RED + f"Duplicado(s) detectado, revisar el file: {rutaEntrada}")
                Oracle_Cerrar_Conexion(conexion, cursor)
                print("Cerramos el programa en el paso2")
                sys.exit(0)

        print(f"OK: No existen duplicados, se podrán subir los {len(sTv.df_Global)} registros")

        # Crea una copia de seguridad: Si existe la copia, la borra y la vuelve a crear)
        backup = f"{sTv.var_Ora_TAB1}_{var_Fechas3}"
        try:
            # Si ya existe, la eliminamos primero
            if existe_tabla(cursor, backup):
                try:
                    cursor.execute(f"DROP TABLE {backup} CASCADE CONSTRAINTS PURGE")
                    print(Fore.CYAN + f"{dt.now().time()} - OK: Tabla de backup existente {backup} eliminada.")
                except Exception as e:
                    print(Fore.RED + f"{dt.now().time()} - Error al eliminar la tabla {backup}: {e}")
                    conexion.rollback()
                    Oracle_Cerrar_Conexion(conexion, cursor)
                    raise

            # Crear tabla vacía con la misma estructura
            cursor.execute(f"CREATE TABLE {backup} AS SELECT * FROM {sTv.var_Ora_TAB1} WHERE 1=0")
            # Copiar datos
            cursor.execute(f"INSERT INTO {backup} SELECT * FROM {sTv.var_Ora_TAB1}")
            conexion.commit()
            print(Fore.CYAN + f"{dt.now().time()} - OK: Se creó la copia de respaldo en oracle: {backup}")
        except Exception as e:
            print(Fore.RED + f"{dt.now().time()} - Error al crear la copia de seguridad: {e}")
            try:
                conexion.rollback()
            except Exception:
                pass
            Oracle_Cerrar_Conexion(conexion, cursor)
            raise

        print(f"OK: Se creó una copia de respaldo en oracle: {sTv.var_Ora_TAB1}_{var_Fechas3}")
        conexion.commit()

        # Oracle, Cierre de conexiones y liberación de memoria:
        Oracle_Cerrar_Conexion(conexion, cursor)
