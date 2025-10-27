import ORACLE_variables as sTv
from   ORACLE_librerias import *
from   ORACLE_conection import *
init(autoreset=True)

# Parámetros 
USER = sTv.var_Ora_UID
PWD = sTv.var_Ora_PWD
DSN = sTv.var_Ora_DNS
TABLE = sTv.var_Ora_TAB1

F_PROCESO   = "2025-10-27"    # OJO hace referencia a la fecha del día en el que se ejecuta el proceso "FPROCESO" no la feha de datos "FDATOS".
TIPO_ACCION = "LISTAR"        # LISTAR | ELIMINAR

def main():
    # Establecer conexión usando tus funciones (sin modificar)
    conexion, cursor = Oracle_Establece_Conexion(DSN, USER, PWD)
    if not conexion or not cursor:
        print("No se pudo establecer la conexión. Abortando.")
        sys.exit(1)
    try:
        if TIPO_ACCION == "LISTAR":
            sql_list = f"SELECT * FROM {TABLE} WHERE TRUNC(FPROCESO) = TRUNC(TO_DATE(:d, 'YYYY-MM-DD'))"
            cursor.execute(sql_list, {"d": F_PROCESO})
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            print(f"\nFilas de la Tabla que coinciden con FPROCESO {F_PROCESO}:\n{df}")

            sql_count = f"SELECT COUNT(*) FROM {TABLE} WHERE TRUNC(FPROCESO) = TRUNC(TO_DATE(:d, 'YYYY-MM-DD'))"
            cursor.execute(sql_count, {"d": F_PROCESO})
            count = cursor.fetchone()[0] or 0
            print(f"\nFilas que coinciden con FPROCESO {F_PROCESO}: {count} registros.\n")
        elif TIPO_ACCION == "ELIMINAR":
            sql_del = f"DELETE FROM {TABLE} WHERE TRUNC(FPROCESO) = TRUNC(TO_DATE(:d, 'YYYY-MM-DD'))"
            cursor.execute(sql_del, {"d": F_PROCESO})
            borradas = cursor.rowcount
            conexion.commit()
            print(f"Operación completada. Filas eliminadas: {borradas}")
        else:
            print("Opción no valida: LISTAR | ELIMINAR ")
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

