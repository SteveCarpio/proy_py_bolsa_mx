#!/bin/bash
#########################################################################################
#
# Planificacón de procesos de BOLSAS
#
#########################################################################################

# Exportar las variables que necesita Oracle
export LD_LIBRARY_PATH="/opt/oracle/instantclient:$LD_LIBRARY_PATH"
export TNS_ADMIN="/opt/oracle/instantclient/network/admin"

# Fuerza al shell a detenerse inmediatamente si cualquier comando devuelve un error (-e)
# Evita referencias a variables no definidas (-u)
# Captura errores en tuberías (pipefail).
set -euo pipefail

# Ruta raiz de los sh a ejecutar
RUTA_RAIZ="/home/robot/Python/proy_py_bolsa_mx/"
DIAS=$1
ENTORNO=$2

# Job a ejecutar en el siguiente orden
JOB1="BIVA.sh"
JOB2="BMV.sh"
JOB3="BOLSAS.sh"
JOB4="ORACLE.sh"
JOB5="EMISORES.sh"

echo "-------------------------------------------------------------"
echo "`date "+%Y-%m-%d %H.%M"`: CRON_BOLSAS INICIO"
echo " "
echo "`date "+%Y-%m-%d %H.%M"`: Ejecutando ${JOB1}"
${RUTA_RAIZ}${JOB1} $DIAS $ENTORNO
echo "`date "+%Y-%m-%d %H.%M"`: ${JOB1} terminó correctamente"
echo "`date "+%Y-%m-%d %H.%M"`: Ejecutando ${JOB2}"
${RUTA_RAIZ}${JOB2} $DIAS $ENTORNO
echo "`date "+%Y-%m-%d %H.%M"`: ${JOB2} terminó correctamente"
echo "`date "+%Y-%m-%d %H.%M"`: Ejecutando ${JOB3}"
${RUTA_RAIZ}${JOB3} $DIAS $ENTORNO
echo "`date "+%Y-%m-%d %H.%M"`: ${JOB3} terminó correctamente"
echo "`date "+%Y-%m-%d %H.%M"`: Ejecutando ${JOB4}"
${RUTA_RAIZ}${JOB4} $DIAS $ENTORNO
echo "`date "+%Y-%m-%d %H.%M"`: ${JOB4} terminó correctamente"
echo "`date "+%Y-%m-%d %H.%M"`: Ejecutando ${JOB5}"
${RUTA_RAIZ}${JOB5} $DIAS $ENTORNO
echo "`date "+%Y-%m-%d %H.%M"`: ${JOB5} terminó correctamente"
echo " "
echo "`date "+%Y-%m-%d %H.%M"`: Todos los programas se ejecutaron con éxito."
echo "`date "+%Y-%m-%d %H.%M"`: CRON_BOLSAS FIN"
