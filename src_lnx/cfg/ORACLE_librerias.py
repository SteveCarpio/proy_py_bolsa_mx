# ----------------------------------------------------------------------------------
#                      LIBRERÍAS NECESARIAS y OPCIONES
# Descripción: Abajo listo las librerías necesarias para su ejecución x pasos
# Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------


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