# ----------------------------------------------------------------------------------------
#  PASO3: Carga de Datos al Servidor Oracle 
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

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso3():

    if len(sTv.df_Global) == 0:
        print(Fore.RED + "No hay datos en el DataFrame, probar a ejecutar el paso1")
    else:

        # Oracle, Parámetros de conexión:
        oracle_dns=sTv.var_Ora_DNS
        oracle_uid=sTv.var_Ora_UID
        oracle_pwd=sTv.var_Ora_PWD

        # Oracle, Establecer Conexión Oracle:
        conexion, cursor=Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

        if (conexion != None) or (cursor != None):
        
            # Importación del DataFrame
            df = sTv.df_Global
            df['FPROCESO'] = dt.now()
            
            # Recorro el DataFrame registro por registro
            for index, row in df.iterrows():
            
                # Tratamiento de valores NaT a None
                v_N=row['N']
                v_CLAVE=row['CLAVE']
                v_SECCION=row['SECCION']
                v_FECHA=row['FECHA']
                v_ASUNTO=row['ASUNTO']
                v_URL=row['URL']
                v_ARCHIVO=row['ARCHIVO']
                v_ORIGEN=row['ORIGEN']
                v_T=row['T']
                v_FILTRO=row['FILTRO']
                v_FPROCESO=row['FPROCESO']
                v_NOTA="CARGA_DIARIA" #  CARGA_HISTORICO | CARGA_DIARIA | CARGA_PUNTUAL
                
                if pd.isna(v_ARCHIVO):
                    v_ARCHIVO=None    

                try:
                    # Ejecución del INSERT SQL
                    cursor.execute(
                        f"""INSERT INTO {sTv.var_Ora_TAB1} (FECHA, N, CLAVE, SECCION, ASUNTO, URL, ARCHIVO, ORIGEN, T, FILTRO, FPROCESO, NOTA) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                        v_FECHA, v_N, v_CLAVE, v_SECCION, v_ASUNTO, v_URL, v_ARCHIVO, v_ORIGEN, v_T, v_FILTRO, v_FPROCESO, v_NOTA
                    )
                    print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({v_FPROCESO})")
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")
                except Exception as e:
                    print(Fore.RED + f"Registro {index + 1} duplicado en el servidor PYTHON ORACLE, no se insertó.")
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")

            # Oracle, Confirma los cambios
            conexion.commit()
        
        # Oracle, Cierre de conexiones y liberación de memoria:
        Oracle_Cerrar_Conexion(conexion, cursor)
