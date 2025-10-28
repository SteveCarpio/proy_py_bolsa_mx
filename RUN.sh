#!/bin/bash
#########################################################################################
#
# Planificacón de procesos de BOLSAS
#
#########################################################################################

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

echo "Ejecutando ${JOB1} "
echo "${RUTA_RAIZ}${JOB1} $DIAS $ENTORNO"
echo "${JOB1} terminó correctamente"
echo " "
echo "Ejecutando ${JOB2} "
echo "${RUTA_RAIZ}${JOB2} $DIAS $ENTORNO"
echo "${JOB2} terminó correctamente"
echo " "
echo "Ejecutando ${JOB3} "
echo "${RUTA_RAIZ}${JOB3} $DIAS $ENTORNO"
echo "${JOB3} terminó correctamente"
echo " "
echo "Ejecutando ${JOB4} "
echo "${RUTA_RAIZ}${JOB4} $DIAS $ENTORNO"
echo "${JOB4} terminó correctamente"
echo " "
echo "Ejecutando ${JOB5} "
echo "${RUTA_RAIZ}${JOB5} $DIAS $ENTORNO"
echo "${JOB5} terminó correctamente"
echo " "
echo "Todos los programas se ejecutaron con éxito."