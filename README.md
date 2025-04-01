# Preparar entorno

### Crear un entorno virtual de python
```sh
python -m venv venv
```

### Visual code studio
    Ctrl + Shift + P
    Buscar "Python: Select Interpreter"
    Seleccionar el que tiene "venv"

### Activar el entorno virtual
```sh
venv\Scripts\activate
```

## Tabajar con el requirements.txt
### Actualizar el requirements.txt
```sh
pip freeze > requirements.txt
```

### Instalar requerimientos
```sh
pip install -r requirements.txt
```


# Preparar fichero Token

## V2
1. Copia el fichero **tealiumTokenV2_example.json** y pegalo en la misma ruta renombrandolo como **tealiumTokenV2.json**
2. Cambia el "<<API_KEY_DE_TEALIUM>>" por tu API KEY obtenida desde tealium
3. Cambia el "<<EMAIL_DEL_USUARIO_DE_LA_API>>" por el email del usuario al que esta ligado la API KEY
4. Cambia el "<<TEALIUM_ACCOUNT>>" por la cuenta de Tealium
5. Guarda el fichero.

## V3
1. Copia el fichero **tealiumTokenV3_example.json** y pegalo en la misma ruta renombrandolo como **tealiumTokenV3.json**
2. Cambia el "<<API_KEY_DE_TEALIUM>>" por tu API KEY obtenida desde tealium
3. Cambia el "<<EMAIL_DEL_USUARIO_DE_LA_API>>" por el email del usuario al que esta ligado la API KEY
4. Cambia el "<<TEALIUM_ACCOUNT>>" por la cuenta de Tealium
5. Dejar el "profiles":{} tal cual está
6. Guarda el fichero.


# Incidencas con Tealium

A continuacion se detallan los problemas encontrados con la API de Tealium q estamos esperando a q nos resuelvan.

## V2

### Error 1
    Al intentar obtener el detalle de una version siempre se obtiene el mensaje de error {'returnCode': 1260, 'message': 'That revision details does not exist'}, confirmado en el tiquet 261008 a la espera de resolución.

## V3

### Error 1
    Cuando recuperas el detalle de una version la información de que entornos se publicó NO es correcta, confirmado en el tiquet 261008 a la espera de resolución.

## Otros
    Esto no es un error en sí pero para dejarlo tambien inventariado ya que lo consultamos y tenemos confirmación de ello, la API no puede hacer acciones a nivel de cuenta p.e: NO es posible obtener el listado de perfiles de una cuenta.

    Falta por aclarar con soporte el uso y valor del parametro tps, tratandolo en tiquet 261324