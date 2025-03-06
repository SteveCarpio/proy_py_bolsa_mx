# Análisis Bolsas de México - BMV y BIVA
<br><br>
----[En-Construcción]----
<br><br>

## Instalar el entorno virtual
pip install virtualenv

## Crear el entorno virtual
virtualenv -p python3 env  

## Activar el entorno virtual
.\env\Scripts\activate

## Salir del entorno virtual
deactivate

## Crear un archivo requerimientos 
pip freeze > requirements.txt

## Compilar
pyinstaller --onefile --name=BMV_Main BMV_Main.py
pyinstaller --onefile --name=BIVA_Main MAIN_Main.py
pyinstaller --onefile --name=BOLSAS_Main BOLSAS_Main.py


