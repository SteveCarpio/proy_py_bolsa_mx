# ----------------------------------------------------------------------------------------
#                                  VARIABLES DE APOYO
# Descripción: Variables necesarias para la ejecución del proceso.
# Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#                          API GOOGLE CHROMEDRIVER
# ----------------------------------------------------------------------------------------
#var_CHROMEDRIVER="C:/MisCompilados/cfg/chromedriver-win32/134/chromedriver.exe"         #   Chrome ver 134... CASA
var_CHROMEDRIVER="C:/MisCompilados/cfg/chromedriver-win32/131/chromedriver.exe"          #   Chrome ver 131... OFICINA

# ----------------------------------------------------------------------------------------
#                          URL WEBSCRAPING
# ----------------------------------------------------------------------------------------
var_WEBSCRAPING1="https://www.biva.mx/empresas/emisoras_inscritas/banco_de_informacion"
var_WEBSCRAPING2="https://www.biva.mx/emisoras/empresas/xls?biva=false&canceladas=false"  # Excel con la Lista de Todos los Emisores

#-----------------------------------------------------------------------------------------
#                          RUTAS DE APOYO
# ----------------------------------------------------------------------------------------
var_RutaRaiz='C:\\MisCompilados\\PROY_BOLSA_MX\\BIVA\\'
var_RutaInforme=f'{var_RutaRaiz}INFORMES\\'
var_RutaWebFiles=f'{var_RutaRaiz}WEBFILES\\'
var_RutaConfig=f'{var_RutaRaiz}CONFIG\\'

# ----------------------------------------------------------------------------------------
#                          VARIABLES DE APOYO
# ----------------------------------------------------------------------------------------
var_NombreEmisores="BIVA_Filtro_Emisores_DEV"
var_WarningEmisores=""

# ----------------------------------------------------------------------------------------
#                          AUTOR
# ----------------------------------------------------------------------------------------
var_sTv1="SteveCarpio-2024"
var_sTv2="stv.madrid@gmail.com" 
