# ----------------------------------------------------------------------------------------
#                      LIBRERÍAS NECESARIAS y OPCIONES
# Descripción: Abajo listo las librerías necesarias para su ejecución x pasos
# Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------


# CARGA DE LIBRERÍAS ---------------------------------------------------------------------
#                                                                 # Ma P0 P1 P2 P3 P4 P5 #
import os                                                         # ma p0 -- -- -- -- -- #
import time                                                       # -- p0 -- -- -- -- -- #
import glob                                                       # -- p0 -- -- -- -- -- #
import pandas as pd                                               # -- -- -- -- -- -- -- #
import requests                                                   # -- -- -- -- -- -- -- #
import re                                                         # -- -- -- -- -- -- -- # 
import smtplib                                                    # -- -- -- -- -- -- -- # 
import sys                                                        # ma -- -- -- -- -- -- #
import subprocess                                                 # -- p0 -- -- -- -- -- #
import winreg                                                     # -- p0 -- -- -- -- -- #
import subprocess                                                 # -- p0 -- -- -- -- -- #
from colorama import init, Fore, Back, Style                      # ma -- -- -- -- -- -- #
from selenium import webdriver                                    # -- -- -- -- -- -- -- #
from selenium.webdriver.chrome.service import Service             # -- -- -- -- -- -- -- #
from selenium.webdriver.chrome.options import Options             # -- -- -- -- -- -- -- #
from selenium.webdriver.support.ui import WebDriverWait           # -- -- -- -- -- -- -- #
from selenium.webdriver.support import expected_conditions as EC  # -- -- -- -- -- -- -- #
from selenium.webdriver.common.by import By                       # -- -- -- -- -- -- -- #
from datetime import datetime as dt                               # ma -- -- -- -- -- -- #
from datetime import timedelta                                    # ma -- -- -- -- -- -- #
from bs4 import BeautifulSoup                                     # -- -- -- -- -- -- -- #
from email.mime.multipart import MIMEMultipart                    # -- -- -- -- -- -- -- #
from email.mime.text import MIMEText                              # -- -- -- -- -- -- -- #
from email.mime.application import MIMEApplication                # -- -- -- -- -- -- -- #
# ----------------------------------------------------------------------------------------


# CUSTOMIZE LAS LIBRERÍAS ---------------------------------------------------------------------------------------------------
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
