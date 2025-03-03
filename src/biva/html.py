from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
import time

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')   # Ignorar certificados
var_CHROMEDRIVER="C:/MisCompilados/cfg/chromedriver-win32/131/chromedriver.exe"   

driver = webdriver.Chrome(service=Service(var_CHROMEDRIVER), options=chrome_options)

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL de la página que deseas descargar
url = 'https://www.biva.mx/empresas/emisoras_inscritas/banco_de_informacion?fechaInicio=2025-02-28&fechaFin=2025-02-28&page=1'

# Abrir la página
driver.get(url)

# Esperar a que el JavaScript cargue el contenido dinámico (ajusta el tiempo según lo necesario)
time.sleep(5)  # Espera 5 segundos (ajusta si es necesario)

# Ahora, puedes obtener el contenido HTML después de que JavaScript se haya ejecutado
html_content = driver.page_source

# Guardar el contenido en un archivo HTML
with open("C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\tmp\\pagina_descargada.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Cerrar el navegador
driver.quit()
