# ----------------------------------------------------------------------------------------
#  PASO2: Validar Datos Locales vs Oracle, comprobamos que no estén en producción los 
#         nuevos registros a anexar.
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.ORACLE_variables as sTv
from   cfg.ORACLE_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------


def Oracle_Establece_Conexion(par_dsn, par_uid, par_pwd, lib_dir=None):
    try:
        # Si tu Instant Client no está en ldconfig, indícalo una vez
        if lib_dir:
            oracledb.init_oracle_client(lib_dir=lib_dir)
        # par_dsn puede ser "host:port/servicename" o un TNS name si está en tnsnames.ora
        conn = oracledb.connect(user=par_uid, password=par_pwd, dsn=par_dsn)
        cur = conn.cursor()
        print(Fore.CYAN + f"{dt.now().time()} - Conexión establecida.")
        return conn, cur
    except oracledb.Error as e:
        print(Fore.RED + f'{dt.now().time()} - Error al conectar con Oracle\n{e}')
        return None, None

# Cierra una conexión a Oracle
def Oracle_Cerrar_Conexion(conn, cur):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print(Fore.CYAN + f"{dt.now().time()} - Conexión cerrada.")
    except oracledb.Error as e:
        print(Fore.RED + f'{dt.now().time()} - Error al cerrar la conexión\n{e}')




# Establece una conexión a Oracle 
def Oracle_Establece_Conexion_old(par_dsn, par_uid,par_pwd):
    try:
        # Cadena de conexión a la base de datos Oracle
        connection_string = f'DSN={par_dsn};UID={par_uid};PWD={par_pwd};'
        # Establecer la conexión y un cursor a la base de datos Oracle
        conexion = pyodbc.connect(connection_string)
        cursor = conexion.cursor()
        print(Fore.CYAN + f"{dt.now().time()} - Conexión establecida.")
        return conexion, cursor
    except pyodbc.Error as e:
        print(Fore.RED + f'{dt.now().time()} - Error al conectar con Oracle \n{e}')
        return None, None 

# Cierra una conexión a Oracle
def Oracle_Cerrar_Conexion_old(conexion, cursor):
    try:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        print(Fore.CYAN + f"{dt.now().time()} - Conexión cerrada. ")
    except pyodbc.Error as e:
        print(Fore.RED + f'{dt.now().time()} - Error al cerrar la conexión \n{e}')

    ### -------------------------------- Inicio del programa ----------------------------

# Valida si existe una tabla en concreto en oracle
def existe_tabla(cursor, nombre_tabla):
    query = f"""
    SELECT table_name FROM user_tables 
    WHERE table_name = UPPER('{nombre_tabla}')
    """
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado is not None
  

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



# Validamos si el registro existe en ORACLE
def existe_en_oracle_old(cursor, row):
    condiciones = """
    SELECT 1 FROM P_BOLSAS_EVENTOS_RELEVANTES
    WHERE FECHA = ?
      AND N = ?
      AND CLAVE = ?
      AND SECCION = ?
      AND ASUNTO = ?
      AND URL = ?
    """
    params = [
        row['FECHA'],
        row['N'],
        row['CLAVE'],
        row['SECCION'],
        row['ASUNTO'],
        row['URL'],
    ]

    # Verificamos si ARCHIVO es None (NULL)
    if row['ARCHIVO'] is None:
        condiciones += " AND ARCHIVO IS NULL"
    else:
        condiciones += " AND ARCHIVO = ?"
        params.append(row['ARCHIVO'])

    condiciones += """
      AND ORIGEN = ?
      AND T = ?
      AND FILTRO = ?
    """
    params.extend([
        row['ORIGEN'],
        row['T'],
        row['FILTRO']
    ])

    cursor.execute(condiciones, params)
    return cursor.fetchone() is not None

        
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

        # Crea una copia de seguridad
        #cursor.execute(f"CREATE TABLE {sTv.var_Ora_TAB1}_{var_Fechas3} AS SELECT * FROM {sTv.var_Ora_TAB1} WHERE 1=0")
        #cursor.execute(f"INSERT INTO {sTv.var_Ora_TAB1}_{var_Fechas3} SELECT * FROM {sTv.var_Ora_TAB1}")

        # Crea una copia de seguridad (Opción 1: si existe, la borra y la vuelve a crear)
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

        
        
        
