# proy_py_bolsa_mx

Este proyecto es una herramienta para analizar datos de la bolsa de valores de México. Utiliza Python para extraer, procesar y visualizar datos financieros.

## Requisitos

- Python 3.6 o superior
- Librerías especificadas en `requirements.txt`
- https://github.com/dreamshao/chromedriver

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/SteveCarpio/proy_py_bolsa_mx.git
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd proy_py_bolsa_mx
    ```
3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso: Hay dos formas de ejecutar el proyecto:

1. Ejecuta el script en este orden para una ejecución en bach:
    ```sh
    python BIVA_Main.py RUN-NO-EMAIL
    python BMV_Main.py RUN-NO-EMAIL
    python BOLSAS_Main.py RUN
    ```
2. Ejecuta el scrip sin parámetros y sigue las instrucciones en la terminal.

- Aplicativo BIVA.
    ```sh
    0 - Ejecutar todos los pasos
    1 - Paso 1 : 
    2 - Paso 2 : 
    n - etc...
    ```
- Aplicativo BMV.
    ```sh
    0 - Ejecutar todos los pasos
    1 - Paso 1 : 
    2 - Paso 2 :
    n - etc...
    ```
- Aplicativo BOLSAS.
    ```sh
    0 - Ejecutar todos los pasos
    1 - Paso 1 : 
    2 - Paso 2 :
    n - etc...
    ```
## Estructura del Proyecto

- `......_Main.py`: Punto de entrada del programa.
- `bmv/ , bmv/ , cfg/  `: Contiene los datos de entrada y salida.
- [src]: Contiene el código fuente del proyecto.
- `tests/`: Contiene los tests del proyecto.

## Contribución

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

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
pyinstaller --onefile --name=BIVA_Main BIVA_Main.py
pyinstaller --onefile --name=BMV_Main BMV_Main.py
pyinstaller --onefile --name=BOLSAS_Main BOLSAS_Main.py

pyinstaller --onefile --clean --noupx BIVA_Main.py
pyinstaller --onefile --clean --noupx BMV_Main.py
pyinstaller --onefile --clean --noupx BOLSAS_Main.py


