#!/bin/bash
#################################################################################
#  Script Bash para ejecutar el job BIVA_Main.py con parámetros
#  específicos y gestionar los logs de salida y error.
#  0 9 * * * /bin/bash /home/robot/Python/proy_py_bolsa_mx/BIVA.sh 1
#  ** esto ejecutará el script todos los días 9:00 AM con la fecha de ayer (1).
#  Autor: Steve Carpio
#  Fecha: 2025-10-27
#################################################################################

# === CONFIGURACIÓN GENERAL ===
NOMBRE_BASH="BIVA.sh"
NOMBRE_JOB="BIVA_Main.py"
RUTA_JOB="/home/robot/Python/proy_py_bolsa_mx/"
RUTA_LOG="/srv/apps/MisCompilados/PROY_BOLSA_MX/BIVA/LOG/"
DIAS=$1
ENTORNO=$2


# === DEFINE FECHA DE EJECUCIÓN RESTANDO DIAS Y DEFINE LOG DE SALIDA ===
fecha=$(date -d "$DIAS days ago" +%F)
exe="${RUTA_JOB}src_lnx/$NOMBRE_JOB"
logBase="${RUTA_LOG}${NOMBRE_JOB%.*}_$fecha"

# === ACTIVAR ENTORNO VIRTUAL ===
source "${RUTA_JOB}venv/bin/activate"

# === CONFIGURAR TERM ===
export TERM=xterm      # Para que no de un mensaje de error en la log "err", desde cron no encuentra esta variable 
# o: export TERM=dumb

# === EJECUCIÓN DEL SCRIPT ===
ahora=$(date +"%Y-%m-%d %H.%M")
runjob="python3 $exe RUN-NO-EMAIL $ENTORNO $fecha"
echo "$ahora: Ini bash $NOMBRE_BASH: $runjob" 
python3 "$exe" "RUN-NO-EMAIL" "$ENTORNO" "$fecha" > "${logBase}_out.log" 2> "${logBase}_err.log"
ahora=$(date +"%Y-%m-%d %H.%M")
echo "$ahora: Fin bash $NOMBRE_BASH: $runjob" 

# === DESACTIVAR ENTORNO VIRTUAL ===
#deactivate