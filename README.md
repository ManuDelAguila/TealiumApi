Preparar entorno

Crear un entorno virtual de python
    python -m venv venv

Visual code
    Ctrl + Shift + P
    Buscar "Python: Select Interpreter"
    Seleccionar el que tiene "venv"

Activar el entorno virtual
    venv\Scripts\activate

Actualizar el requirements.txt
    pip freeze > requirements.txt

Instalar requerimientos
    pip install -r requirements.txt


Preparar fichero Token

V2
    1. Copia el fichero tealiumTokenV2_example.json y pegalo en la misma ruta renombrandolo como tealiumTokenV2.json
    2. Cambia el "<<API_KEY_DE_TEALIUM>>" por tu API KEY obtenida desde tealium
    3. Cambia el "<<EMAIL_DEL_USUARIO_DE_LA_API>>" por el email del usuario al que esta ligado la API KEY
    4. Guarda el fichero.