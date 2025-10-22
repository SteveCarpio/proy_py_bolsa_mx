# -------------------------------------------------------------------------------------------------
#                      LIBRERIAS NECESARIAS y OPCIONES
# Descripción: Abajo listo las librerías necesarias para su ejecución x pasos
# Autor: SteveCarpio-2025
# -------------------------------------------------------------------------------------------------


# CARGA DE LIBRERIAS ------------------------------------------------------------------------------
#                                                                 # Ma P0 P1 P2 P3 P4 P5 P6 P7 P8 #
import io                                                         # ma -- -- -- -- -- -- -- -- -- #
import os                                                         # ma p0 -- -- -- -- -- p6 -- p8 #
import time                                                       # -- p0 p1 -- -- -- -- -- -- -- #
import glob                                                       # -- p0 -- -- -- -- -- -- -- -- #
import pandas as pd                                               # -- -- -- p2 p3 p4 p5 p6 p7 p8 #
import requests                                                   # -- -- -- -- -- -- p5 -- -- -- #
import re                                                         # -- -- -- -- -- -- -- p6 -- -- # 
import smtplib                                                    # -- -- -- -- -- -- -- -- -- p8 # 
import sys                                                        # ma -- -- -- -- -- -- -- -- -- #
import subprocess                                                 # -- p0 -- -- -- -- -- -- -- -- #
import winreg                                                     # -- p0 -- -- -- -- -- -- -- -- #
from colorama import init, Fore, Back, Style                      # ma -- -- -- -- -- -- -- -- -- #
from selenium import webdriver                                    # -- -- p1 -- -- -- -- -- -- -- #
from selenium.webdriver.chrome.service import Service             # -- -- p1 -- -- -- -- -- -- -- #
from selenium.webdriver.chrome.options import Options             # -- -- p1 -- -- -- -- -- -- -- #
from selenium.webdriver.support.ui import WebDriverWait           # -- -- p1 -- -- -- -- -- -- -- #
from selenium.webdriver.support import expected_conditions as EC  # -- -- p1 -- -- -- -- -- -- -- #
from selenium.webdriver.common.by import By                       # -- -- p1 -- -- -- -- -- -- -- #
from datetime import datetime as dt                               # ma -- -- -- -- -- -- -- p7 -- #
from datetime import timedelta                                    # ma -- -- -- -- p4 -- -- p7 -- #
from bs4 import BeautifulSoup                                     # -- -- -- -- -- -- -- p6 -- -- #
from email.mime.multipart import MIMEMultipart                    # -- -- -- -- -- -- -- -- -- p8 #
from email.mime.text import MIMEText                              # -- -- -- -- -- -- -- -- -- p8 #
from email.mime.application import MIMEApplication                # -- -- -- -- -- -- -- -- -- p8 #
# -------------------------------------------------------------------------------------------------


# CUSTOMIZAR LAS LIBRERIAS ---------------------------------------------------------------------------------------------------
chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2 ,       # 2 = Bloquear  Imágenes
         "profile.managed_default_content_settings.javascript": 1}    # 1 = Habilitar JavaScript 
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-extensions")          # Desactivar extensiones
chrome_options.add_argument("--log-level=3")                 # Suprime los mensajes de log (nivel de error: WARNING y superior)
chrome_options.add_argument("--disable-sync")                # Desactivar la sincronización con el perfil de usuario
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Desactivar animaciones
chrome_options.add_argument("--disable-features=VizDisplayCompositor")       # Desactivar animaciones
chrome_options.add_argument("--disable-plugins")             # Desactivar plugins
chrome_options.add_argument("--incognito")                   # Usar modo incógnito
chrome_options.add_argument("--headless")                    # Ejecutar SIN interfaz gráfica :  carga más rápido
chrome_options.add_argument("--disable-gpu")                 # Desactivar uso de GPU         :  carga más rápido
chrome_options.add_argument('--ignore-certificate-errors')   # Ignorar certificados   
#chrome_options.add_argument("--user-data-dir=/path/to/a/clean/profile")   # Con esta option me hace cosas raras
# ----------------------------------------------------------------------------------------------------------------------------
