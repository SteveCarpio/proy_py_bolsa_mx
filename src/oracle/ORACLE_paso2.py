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

# Establece una conexión a Oracle 
def Oracle_Establece_Conexion(par_dsn, par_uid,par_pwd):
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
def Oracle_Cerrar_Conexion(conexion, cursor):
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
  
# Validamos si el registro existe en ORACLE
def existe_en_oracle(cursor, row):
    query = """
    SELECT 1 FROM P_BOLSAS_EVENTOS_RELEVANTES
    WHERE FECHA = ?
      AND N = ?
      AND CLAVE = ?
      AND SECCION = ?
      AND ASUNTO = ?
      AND URL = ?
      AND ARCHIVO IS ?
      AND ORIGEN = ?
      AND T = ?
      AND FILTRO = ?
    """
    cursor.execute(query, (
        row['FECHA'],
        row['N'],
        row['CLAVE'],
        row['SECCION'],
        row['ASUNTO'],
        row['URL'],
        row['ARCHIVO'],  # Comparación con IS para aceptar NULL correctamente
        row['ORIGEN'],
        row['T'],
        row['FILTRO']
    ))
    return cursor.fetchone() is not None

        
# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2():

    if len(sTv.df_Global) == 0:
        print(Fore.RED + "No hay datos en el DataFrame, probar a ejecutar el paso1")
    else:

        # Oracle, Parámetros de conexión:
        oracle_dns=sTv.var_Ora_DNS
        oracle_uid=sTv.var_Ora_UID
        oracle_pwd=sTv.var_Ora_PWD

        # Oracle, Establecer Conexión Oracle:
        conexion, cursor=Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

        # Validamos si existe o no una tabla Oracle    
        if cursor:
            if existe_tabla(cursor, sTv.var_Ora_TAB1):
                print(f"La tabla {sTv.var_Ora_TAB1} existe.")
            else:
                print(Fore.RED + f"La tabla {sTv.var_Ora_TAB1} NO existe.")
                sys.exit(0)

        # Validamos si el registro existe en ORACLE
        duplicados = []

        # Validar duplicados
        for idx, row in sTv.df_Global.iterrows():
            if existe_en_oracle(cursor, row):
                print(Fore.RED + f"\nDuplicado detectado (no se subirá): fila {idx}")
                print(row)
                duplicados.append(row)
      
        # Oracle, Cierre de conexiones y liberación de memoria:
        Oracle_Cerrar_Conexion(conexion, cursor)

        # Mostrar total
        if len(duplicados > 0):
            print(Fore.RED + f"\nTotal duplicados detectados: {len(duplicados)}")
            sys.exit(0)
