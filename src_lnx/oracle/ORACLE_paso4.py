# ----------------------------------------------------------------------------------------
#  PASO4: Borro las tablas que se acumulan, nos quedamos con las N ultimas => "mantener"
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.ORACLE_variables as sTv
from   cfg.ORACLE_librerias import *
from   cfg.ORACLE_conection import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

def borrar_tablas_antiguas(conexion, cursor, mantener=15):
    # 1️⃣ Obtener las "N" tablas y ordenarlas por fecha
    query = """
        SELECT table_name
        FROM (
            SELECT table_name,
                   ROW_NUMBER() OVER (ORDER BY TO_DATE(SUBSTR(table_name, -8), 'YYYYMMDD') DESC) AS rn
            FROM user_tables
            WHERE table_name LIKE 'P_BOLSAS_EVENTOS_RELEVANTES_%'
        )
        WHERE rn > :mantener
    """
    cursor.execute(query, mantener=mantener)
    tablas_a_borrar = [row[0] for row in cursor.fetchall()]

    if not tablas_a_borrar:
        print("No hay tablas antiguas para borrar.")
        return

    print("Tablas a borrar:", tablas_a_borrar)

    # 2️⃣ Borrar tablas
    for tabla in tablas_a_borrar:
        drop_sql = f'DROP TABLE {tabla} CASCADE CONSTRAINTS'
        print(f'Ejecutando: {drop_sql}')
        cursor.execute(drop_sql)
    
    # 3️⃣ Confirmar cambios
    conexion.commit()
    print("Tablas antiguas eliminadas correctamente.")


# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso4():

    if len(sTv.df_Global) == 0:
        print(Fore.RED + "No hay datos en el DataFrame, probar a ejecutar el paso1")
    else:

        # Oracle, Parámetros de conexión:
        oracle_dns = sTv.var_Ora_DNS
        oracle_uid = sTv.var_Ora_UID
        oracle_pwd = sTv.var_Ora_PWD

        # Establecer Conexión Oracle
        conexion, cursor = Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)
        try:
            # Borrar versiones de bbdd oracle
            borrar_tablas_antiguas(conexion, cursor, mantener=15)
        finally:
            # Cierro Conexión Oracle
            Oracle_Cerrar_Conexion(conexion, cursor)
            
