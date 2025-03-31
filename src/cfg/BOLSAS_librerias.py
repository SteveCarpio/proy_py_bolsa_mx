# -------------------------------------------------------------------------------------
#                      LIBRERÍAS NECESARIAS
# Descripción: Abajo listo las librerías necesarias para su ejecución x pasos
# Autor: SteveCarpio-2025
# -------------------------------------------------------------------------------------

# CARGA DE LIBRERÍAS ------------------------------------------------------------------
#                                                                 # Ma P0 P1 P2 P3 P4 #
import io                                                         # ma -- -- -- -- -- #
import os                                                         # ma p0 -- -- p3 p4 #
import time                                                       # -- -- -- -- -- -- #
import glob                                                       # -- p0 -- -- -- -- #
import pandas as pd                                               # -- -- -- -- -- p4 #
import smtplib                                                    # -- -- -- -- -- p4 # 
import sys                                                        # -- -- -- -- -- -- #
import subprocess                                                 # -- -- p1 p2 -- -- #
import shutil                                                     # -- -- -- -- p3 -- #
from colorama import init, Fore, Back, Style                      # ma p0 -- -- -- -- #
from datetime import datetime as dt                               # ma -- -- -- -- -- #
from datetime import timedelta                                    # ma -- -- -- -- -- #
from email.mime.multipart import MIMEMultipart                    # -- -- -- -- -- p4 #
from email.mime.text import MIMEText                              # -- -- -- -- -- p4 #
from email.mime.application import MIMEApplication                # -- -- -- -- -- p4 #
# -------------------------------------------------------------------------------------
