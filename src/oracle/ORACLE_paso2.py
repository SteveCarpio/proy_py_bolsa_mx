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

# 1 - def Oracle_Establece_Conexión(par_dsn , par_uid , par_pwd) 
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

# 2 - def Oracle_Cerrar_Conexion(conexion , cursor)
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

  

        
# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2():

    # Oracle, Parámetros de conexión:
    oracle_dns=sTv.var_Ora_DNS
    oracle_uid=sTv.var_Ora_UID
    oracle_pwd=sTv.var_Ora_PWD

    # Oracle, Establecer Conexión Oracle:
    conexion, cursor=Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

    print(conexion)
    print(cursor)

    '''

    if (conexion != None) or (cursor != None):
        # Parámetros otros, file 'txt' y variables de apoyo:
        var_periodo = PAR7    # var_periodo = int(f'{dt.now().year}{dt.now().month}')
        var_fecha_proceso = dt.now().date()
        files_csv = PAR2
        file_path = f"C:\\MisCompilados\\PROY_BIACTIVOS\\file_in\\{files_csv}.txt"

        # Importación del fichero "FileN.txt" en un DataFrame:
        df = pd.read_csv(file_path, sep='\t', header=None,
            names=['NUMERO_DE_OPERACION', 'NUMERO_DE_CUOTA', 'FECHA_DE_VENCIMIENTO', 'CAPITAL', 'INTERES', 'IVA',
                'TOTAL_CUOTA','TOTAL_RECAUDADO', 'FECHA_DE_PAGO', 'FECHA_DESCUENTO_DE_NOMINA', 'ESTADO_DEL_PAGO'],
            dtype={'NUMERO_DE_OPERACION': str, 'NUMERO_DE_CUOTA': int, 'CAPITAL': float, 'INTERES': float, 'IVA': float, 
                'TOTAL_CUOTA':float, 'TOTAL_RECAUDADO':float,'ESTADO_DEL_PAGO':str ,'ESTADO_DEL_PAGO':str},
            parse_dates=['FECHA_DE_VENCIMIENTO','FECHA_DE_PAGO','FECHA_DESCUENTO_DE_NOMINA'],
            dayfirst=True
        )

        # Imprime log del estado del Hilo
        print(f'    Hilo[{PAR11}] - {dt.now().time()} - Insert Into Oracle {PAR3} {len(df):,} records From {PAR2}.txt'.replace(",","."))

        ### -------------------------------------- Oracle -----------------------------------
        # Parámetros necesarios para Exportación del DataFrame al Oracle de TdA:
        table_name = PAR3

        # Oracle, Recorro el DataFrame registro por registro
        for index, row in df.iterrows():
            # Tratamiento de valores NaT a None
            tmpFECHA1=row['FECHA_DE_PAGO']
            tmpFECHA2=row['FECHA_DESCUENTO_DE_NOMINA']
            if pd.isna(tmpFECHA1):
                tmpFECHA1=None
            if pd.isna(tmpFECHA2):
                tmpFECHA2=None    
            # Ejecución del INSERT SQL
            cursor.execute(
                f"""INSERT INTO {table_name} (NUMERO_DE_OPERACION, NUMERO_DE_CUOTA, FECHA_DE_VENCIMIENTO, CAPITAL, INTERES, IVA,
                TOTAL_CUOTA, TOTAL_RECAUDADO, FECHA_DE_PAGO, FECHA_DESCUENTO_DE_NOMINA, ESTADO_DEL_PAGO, PERIODO, FECHA_PROCESO) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                row['NUMERO_DE_OPERACION'], row['NUMERO_DE_CUOTA'], row['FECHA_DE_VENCIMIENTO'], row['CAPITAL'], row['INTERES'], 
                row['IVA'], row['TOTAL_CUOTA'], row['TOTAL_RECAUDADO'], tmpFECHA1, tmpFECHA2, 
                row['ESTADO_DEL_PAGO'], var_periodo, var_fecha_proceso
            )

        # Oracle, Confirma los cambios
        conexion.commit()
        print(f'    Hilo[{PAR11}] - {dt.now().time()} - Commit OK')

        
    '''
    # Oracle, Cierre de conexiones y liberación de memoria:
    Oracle_Cerrar_Conexion(conexion, cursor)
