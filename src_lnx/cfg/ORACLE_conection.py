
from   cfg.ORACLE_librerias import *

def Oracle_Establece_Conexion(par_dsn, par_uid, par_pwd):
    try:
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