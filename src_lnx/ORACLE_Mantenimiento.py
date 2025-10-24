#!/usr/bin/env python3
"""
program.py - Elimina los registros de un día concreto (FPROCESO) usando
las funciones existentes Oracle_Establece_Conexion y Oracle_Cerrar_Conexion
tal cual las tienes en tu proyecto.

Ajustes mínimos que puedes editar en el código:
- Cambia DSN, USER, PWD por tus credenciales.
- Cambia TARGET_DATE a la fecha que quieras borrar (YYYY-MM-DD).
- Ajusta la línea de import si las funciones están en otro módulo.
"""

# CARGA DE LIBRERÍAS ---------------------------------------------------------------
#                                                                 # Ma P0 P1 P2 P3 #
import sys                                                        # ma -- -- -- -- #
import re                                                         # ma -- -- -- -- #
import os                                                         # ma p0 -- -- -- #
import time                                                       # -- p0 -- -- -- #
import glob                                                       # -- p0 -- -- -- #
import pandas as pd                                               # -- -- p1 p2 -- #
#import pyodbc                                                    # -- -- -- p2 p3 #  OLD: esta ya no se usa
import oracledb                                                   # -- -- -- p2 p3 #  NEW: 
from colorama import init, Fore, Back, Style                      # ma p0 p1 -- -- #
from datetime import datetime as dt                               # ma -- -- -- -- #
from datetime import timedelta                                    # ma -- -- -- -- #

# ----------------------------------------------------------------------------------

import sys
import oracledb
from colorama import init, Fore, Back, Style 
init(autoreset=True)

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

# Parámetros (edita aquí)
DSN = "COMUN"      # cambiar si corresponde
USER = "PYDATA"                  # cambiar
PWD = "PYDATA"                # cambiar
TABLE = "P_BOLSAS_EVENTOS_RELEVANTES"
TARGET_DATE = "2025-10-24"  # <-- pone la fecha que quieras eliminar

def main():
    # Establecer conexión usando tus funciones (sin modificar)
    conexion, cursor = Oracle_Establece_Conexion(DSN, USER, PWD)

    if not conexion or not cursor:
        print("No se pudo establecer la conexión. Abortando.")
        sys.exit(1)

    try:
        # DELETE sencillo: compara solo la parte fecha del timestamp
        sql = f"DELETE FROM {TABLE} WHERE TRUNC(FPROCESO) = TRUNC(TO_DATE(:d, 'YYYY-MM-DD'))"
        cursor.execute(sql, {"d": TARGET_DATE})
        borradas = cursor.rowcount
        conexion.commit()
        print(f"Operación completada. Filas eliminadas: {borradas}")
    except Exception as e:
        # Si hay error, intentar rollback y mostrarlo
        try:
            conexion.rollback()
        except Exception:
            pass
        print("Error al ejecutar DELETE:", e)
        raise
    finally:
        # Cerrar conexión usando tu función (sin modificar)
        Oracle_Cerrar_Conexion(conexion, cursor)

if __name__ == "__main__":
    main()