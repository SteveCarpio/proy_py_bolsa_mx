# ----------------------------------------------------------------------------------------
#  PASO3: Carga de Datos al Servidor Oracle 
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.ORACLE_variables as sTv
from   cfg.ORACLE_librerias import *
from   cfg.ORACLE_conection import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

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

            # Agregar variable FPROCESO
            fecha_dt = pd.to_datetime(var_Fechas3, format='%Y%m%d')  # Convertirla a datetime (solo fecha)
            df['FPROCESO'] = fecha_dt

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

                    cursor.execute(sql, params) # type: ignore

                    print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({v_FPROCESO})") # type: ignore 
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")

                except Exception as e:
                    # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                    print(Fore.RED + f"Registro {index + 1} no insertado en el servidor PYTHON ORACLE: {e}") # type: ignore
                    print(Fore.WHITE + f"  {v_N} - {v_CLAVE} - {v_SECCION} - {v_FECHA} - {v_ASUNTO}")
                    print(Fore.WHITE + f"  {v_URL} - {v_ARCHIVO} - {v_ORIGEN} - {v_T} - {v_FILTRO} - {v_NOTA}\n")

            # Oracle, Confirma los cambios
            conexion.commit() # type: ignore
        
        # Tratamiento del fichero de Origen:  BOLSAS_AAAAMMDD.xlsx
        fileOld1 = os.path.join(sTv.var_RutaIN, f'{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        fileNew1 = os.path.join(sTv.var_RutaInforme, f'{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        fileNew2 = os.path.join(sTv.var_RutaInforme, f'ora_{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        shutil.copy2(fileOld1, sTv.var_RutaInforme)   # Copio    fichero origen a destino    # type: ignore
        os.rename(fileNew1, fileNew2)                 # Renombro fichero destino

        # Tratamiento del fichero de Origen:  BOLSAS_AAAAMMDD.xlsx
        #fileOld = os.path.join(sTv.var_RutaIN, f'{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        #fileNew = os.path.join(sTv.var_RutaIN, f'ora_{sTv.var_Files_IN}_{var_Fechas3}.xlsx')
        #os.rename(fileOld, fileNew)                  # Renombro fichero origen
        #shutil.copy2(fileNew, sTv.var_RutaInforme)   # Copio    fichero origen a destino    # type: ignore
        #os.remove(fileNew)                           # Elimino  fichero origen

        # Cierro de conexiones Oracle y libero memoria
        Oracle_Cerrar_Conexion(conexion, cursor)
