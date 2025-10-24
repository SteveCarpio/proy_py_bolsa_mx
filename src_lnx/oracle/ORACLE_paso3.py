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

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso3(var_Fechas3):

    if len(sTv.df_Global) == 0:
        print(Fore.RED + "No hay datos en el DataFrame, probar a ejecutar el paso1")
    else:

        # Oracle, Parámetros de conexión:
        oracle_dns = sTv.var_Ora_DNS
        oracle_uid = sTv.var_Ora_UID
        oracle_pwd = sTv.var_Ora_PWD

        # Oracle, Establecer Conexión Oracle:
        conexion, cursor = Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

        if (conexion != None) or (cursor != None):

            # Importación del DataFrame
            df = sTv.df_Global.copy()
            df['FPROCESO'] = dt.now()

            # Recorro el DataFrame registro por registro
            for index, row in df.iterrows():

                # Tratamiento de valores NaT a None
                v_N = row['N']
                v_CLAVE = row['CLAVE']
                v_SECCION = row['SECCION']
                v_FECHA = row['FECHA']
                v_ASUNTO = row['ASUNTO']
                v_URL = row['URL']
                v_ARCHIVO = row['ARCHIVO']
                v_ORIGEN = row['ORIGEN']
                v_T = row['T']
                v_FILTRO = row['FILTRO']
                v_FPROCESO = row['FPROCESO']
                v_NOTA = "CARGA_DIARIA"  #  CARGA_HISTORICO | CARGA_DIARIA | CARGA_PUNTUAL

                # Normalizar NaN/NaT a None
                if pd.isna(v_ARCHIVO):
                    v_ARCHIVO = None
                if pd.isna(v_FECHA):
                    v_FECHA = None
                if pd.isna(v_ASUNTO):
                    v_ASUNTO = None
                # (añade más conversiones si alguna otra columna puede ser NaN/NaT)

                try:
                    # Ejecutar INSERT con binds nombrados (oracledb)
                    sql = f"""
                    INSERT INTO {sTv.var_Ora_TAB1}
                      (FECHA, N, CLAVE, SECCION, ASUNTO, URL, ARCHIVO, ORIGEN, T, FILTRO, FPROCESO, NOTA)
                    VALUES
                      (:FECHA, :N, :CLAVE, :SECCION, :ASUNTO, :URL, :ARCHIVO, :ORIGEN, :T, :FILTRO, :FPROCESO, :NOTA)
                    """

                    params = {
                        "FECHA": v_FECHA,
                        "N": v_N,
                        "CLAVE": v_CLAVE,
                        "SECCION": v_SECCION,
                        "ASUNTO": v_ASUNTO,
                        "URL": v_URL,
                        "ARCHIVO": v_ARCHIVO,
                        "ORIGEN": v_ORIGEN,
                        "T": v_T,
                        "FILTRO": v_FILTRO,
                        "FPROCESO": v_FPROCESO,
                        "NOTA": v_NOTA
                    }

                    cursor.execute(sql, params)

                    print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({v_FPROCESO})")
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")

                except Exception as e:
                    # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                    print(Fore.RED + f"Registro {index + 1} no insertado en el servidor PYTHON ORACLE: {e}")
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")

            # Oracle, Confirma los cambios
            conexion.commit()

        # Renombro el file de entrada para que conste como leído
        fileOld = os.path.join(sTv.var_RutaIN, f'{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        fileNew = os.path.join(sTv.var_RutaIN, f'ora_{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        os.rename(fileOld, fileNew)

        # Oracle, Cierre de conexiones y liberación de memoria:
        Oracle_Cerrar_Conexion(conexion, cursor)



def sTv_paso3_old(var_Fechas3):

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
        
        # Renombro el file de entrada para que conste como leído
        fileOld = os.path.join(sTv.var_RutaIN, f'{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        fileNew = os.path.join(sTv.var_RutaIN, f'ora_{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        os.rename(fileOld, fileNew)

        # Oracle, Cierre de conexiones y liberación de memoria:
        Oracle_Cerrar_Conexion(conexion, cursor)
