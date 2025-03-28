import requests
import json
import os
import time


# Archivo para guardar los datos del token
token_file = "v2/tealiumTokenV2.json"
max_retries = 1

# Variables globales
api_key = None
username = None
account = None
jwt = None


def guardar_datos():
    '''
    Guarda los datos de la API Key, el usuario, el account de tealium y el token en un archivo JSON.
    '''
    with open(token_file, "w") as file:
        json.dump({
            "api_key": api_key,
            "username": username,
            "account": account,
            "token": jwt
        }, file, indent=4)

def cargar_datos():
    '''
    Carga los datos de la API Key, el usuario y el token desde un archivo JSON.
    Los datos cargados se guardan en las variables globales.
    '''
    global api_key, username, account, jwt
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            data = json.load(file)
            api_key = data["api_key"]
            username = data["username"]
            account = data["account"]
            jwt = data["token"]

def obtener_jwt_y_url_base_tealium():
    """
    Obtiene el JWT a partir del API Key.
    """
    global jwt
    url = f"https://api.tealiumiq.com/v2/auth"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": username,
        "key": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        jwt = response_json["token"]
        guardar_datos()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el JWT: {e}")

def obtener_versiones(profile, retries=0):
    '''
    Obetiene la lista de versiones del perfil
    '''
    url = f"https://api.tealiumiq.com/v2/manifest/accounts/{account}/profiles/{profile}/revisions"
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                obtener_jwt_y_url_base_tealium()
                return obtener_versiones(profile, retries + 1)
        print(f"Error al obtener la lista de perfiles: {e}")
        return []

def obtener_detalle_version(profile, revision, retries=0):
    '''
    Obtiene el detalle de una version.
    
    !IMPORTANTE: Actaualmente esta llamada no funciona Tealium lo esta revisando
    '''
    url = f"https://api.tealiumiq.com/v2/manifest/accounts/{account}/profiles/{profile}/revisions/{revision}/details"
    print(f"Url revision detail: {url}")
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(response.json())
        #return response.json()["profiles"]
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al obtener el detalle de la revisión {revision}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al obtener el detalle de la revisión: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                obtener_jwt_y_url_base_tealium()
                return obtener_detalle_version(profile, retries + 1)
        #return None
    

cargar_datos()
profile = "manu"

print(f"Cuenta es {account}")
print(f"Usuario es {username}")

listadoVersiones = obtener_versiones(profile)
print(listadoVersiones)

if len(listadoVersiones) > 0:
    version = listadoVersiones[0]
    obtener_detalle_version(profile, version)