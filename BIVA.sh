#!/bin/bash
# === CONFIGURACIÓN GENERAL ===
NOMBRE_JOB="BIVA_Main.py"
RUTA_JOB="/home/robot/Python/proy_py_bolsa_mx/"
RUTA_LOG="/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/LOG/"
DIAS=$1

# === DEFINE FECHA DE EJECUCIÓN RESTANDO DIAS Y DEFINE LOG DE SALIDA ===
fecha=$(date -d "$DIAS days ago" +%F)
exe="${RUTA_JOB}src_lnx/$NOMBRE_JOB"
logBase="${RUTA_LOG}${NOMBRE_JOB%.*}_$fecha"

# === ACTIVAR ENTORNO VIRTUAL ===
source "${RUTA_JOB}venv/bin/activate"

# === EJECUCIÓN DEL SCRIPT ===
echo "Iniciando job: python3 $exe RUN-NO-EMAIL PRO $fecha"
echo "Iniciando job: python3 $exe RUN-NO-EMAIL PRO $fecha" > "${logBase}_out.log" 2> "${logBase}_err.log"
#python3 "$exe" "RUN-NO-EMAIL" "PRO" "$fecha" > "${logBase}_out.log" 2> "${logBase}_err.log"

# === DESACTIVAR ENTORNO VIRTUAL ===
deactivate