import requests
import json
import os
import time
from datetime import datetime

# Archivo para guardar los datos del token
token_file = "v3/tealiumTokenV3.json"
max_retries = 1

# Variables globales
api_key = None
username = None
account = None
profiles_data = {}

def guardar_datos():
    """
    Guarda el api_key, username, account y los datos de los perfiles en un archivo.
    """
    with open(token_file, "w") as file:
        json.dump({
            "api_key": api_key,
            "username": username,
            "account": account,
            "profiles": profiles_data
        }, file, indent=4)

def cargar_datos():
    """
    Carga el api_key, username, account y los datos de los perfiles desde un archivo.
    """
    global api_key, username, account, profiles_data
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            data = json.load(file)
            api_key = data["api_key"]
            username = data["username"] 
            account = data["account"]
            profiles_data = data["profiles"]

def obtener_jwt_y_url_base_tealium(profile):
    """
    Obtiene el JWT y la URL base de Tealium a partir del API Key y account, teniendo en cuenta que es para un perfil concreto.
    """
    global profiles_data
    url = f"https://platform.tealiumapis.com/v3/auth/accounts/{account}/profiles/{profile}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": username,
        "key": api_key
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        token = response_json["token"]
        url_base = response_json["host"]
        profiles_data[profile] = {"token": token, "url_base": url_base}
        guardar_datos()
        return token, url_base
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el JWT y la URL base: {e}")
        return None, None

def obtener_versiones(profile, retries=0):
    """
    Obtiene la lista de versiones de un perfil de Tealium (API v3).
    """
    jwt = profiles_data.get(profile, {}).get("token")
    url_base = profiles_data.get(profile, {}).get("url_base")
    
    if not jwt or not url_base:
        jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
    
    url = f"https://{url_base}/v3/tiq/accounts/{account}/profiles/{profile}?includes=versionIds"
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        #print(json.dumps(response.json(), indent=4, sort_keys=True))
        return response.json()["versionIds"]
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al obtener versiones del perfil {profile}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al obtener el detalle de la revisión: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
                if jwt and url_base:
                    return obtener_versiones(profile, retries + 1)
        print(f"Error al obtener la lista de versiones: {e}")
        return []

def obtener_detalle_versions(profile, versionId, retries=0):
    """
    Obtiene el detalle de una version de un perfil de Tealium (API v3).
    """
    jwt = profiles_data.get(profile, {}).get("token")
    url_base = profiles_data.get(profile, {}).get("url_base")
    
    if not jwt or not url_base:
        jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
    
    url = f"https://{url_base}/v3/tiq/accounts/{account}/profiles/{profile}?publishVersion={versionId}"
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        #print(json.dumps(response.json(), indent=4, sort_keys=True))
        return response.json()["versionDetails"]
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al obtener detalle versiones del perfil {profile} y version {versionId}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al obtener el detalle de la revisión: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
                if jwt and url_base:
                    return obtener_detalle_versions(profile, versionId, retries + 1)
        print(f"Error al obtener la lista de versiones: {e}")
        return {}
    
def obtener_versiones_entorno(profile, fechaAny, fechaMes, publishLocation):
    '''
    Obtiene las versiones de un perfil que se han publicado para un entorno concreto filtrando por el mes indicado.

    !IMPORTANTE: De momento parece haber un bug con la información que devuelve la API de Tealium y no indica correctamente en que entornos se publicó esa versión.
    '''
    listadoVersiones = obtener_versiones(profile)
    print(listadoVersiones)

    #Filtrar las versiones por año y mes
    versiones_filtradas = [version for version in listadoVersiones if version.startswith(fechaAny + fechaMes)]
    print("Versiones filtradas:", versiones_filtradas)

    #Obtener el detalle de las versiones
    mensajes = []
    for version in versiones_filtradas:
        time.sleep(1)
        detalleVersion = obtener_detalle_versions(profile, version)
        if detalleVersion:
            if(detalleVersion["publishedLocations"][publishLocation]):
                fecha = datetime.strptime(version, "%Y%m%d%H%M").strftime("%d/%m/%Y")
                mensaje = f"Se ha publicado a {publishLocation} en la fecha {fecha} con la siguiente nota: {detalleVersion["notes"]}"
                mensajes.append(mensaje)
            
    print(mensajes)

def obtener_detalle_tags(profile, retries=0):
    """
    Obtiene el detalle de una version de un perfil de Tealium (API v3).
    """
    jwt = profiles_data.get(profile, {}).get("token")
    url_base = profiles_data.get(profile, {}).get("url_base")
    
    if not jwt or not url_base:
        jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
    
    url = f"https://{url_base}/v3/tiq/accounts/{account}/profiles/{profile}?includes=tags"
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=4, sort_keys=True))
        return response.json()["tags"]
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al obtener versiones del perfil {profile}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al obtener el detalle de la revisión: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
                if jwt and url_base:
                    return obtener_detalle_tags(profile, retries + 1)
        print(f"Error al obtener la lista de versiones: {e}")
        return []

def obtener_detalle_loadRules(profile, retries=0):
    """
    Obtiene el detalle de una version de un perfil de Tealium (API v3).
    """
    jwt = profiles_data.get(profile, {}).get("token")
    url_base = profiles_data.get(profile, {}).get("url_base")
    
    if not jwt or not url_base:
        jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
    
    url = f"https://{url_base}/v3/tiq/accounts/{account}/profiles/{profile}?includes=loadRules"
    #print(url)
    headers = {"Authorization": f"Bearer {jwt}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=4, sort_keys=True))
        return response.json()["loadRules"]
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al obtener versiones del perfil {profile}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al obtener el detalle de la revisión: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
                if jwt and url_base:
                    return obtener_detalle_loadRules(profile, retries + 1)
        print(f"Error al obtener la lista de versiones: {e}")
        return []

def actualizar_load_rule(profile, json_data, tps_value, retries=0):
    """
    Actualiza un load rule en Tealium.

    !IMPORTANTE: Siempre da error 400 Invalid request body, reportado  a Tealium.
    """
    jwt = profiles_data.get(profile, {}).get("token")
    url_base = profiles_data.get(profile, {}).get("url_base")
    
    if not jwt or not url_base:
        jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
    
    url = f"https://{url_base}/v3/tiq/accounts/{account}/profiles/{profile}?tps={tps_value}"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(json_data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        try:
            error_response = response.json()
            print(f"Error al actualizar la Load Rule {profile}: {error_response}")
        except json.JSONDecodeError:
            print(f"Error al actualizar la Load Rule: {e}")
        if response.status_code == 401:  # Unauthorized
            print("Token expirado, obteniendo un nuevo token...")
            if retries < max_retries:
                time.sleep(1)
                jwt, url_base = obtener_jwt_y_url_base_tealium(profile)
                if jwt and url_base:
                    return actualizar_load_rule(profile, json_data, tps_value, retries + 1)
        print(f"Error al actualizar la Load Rule: {e}")
        return {}
    
####
#
#   Llamadas a las funciones
#
##

# Cargar los datos desde el archivo
cargar_datos()

# Definir el perfil que se desea consultar
profile = "manu"

#### Funcionalidad para obtener el listado de versioines de un perfil y entorno.
#obtener_versiones_entorno(profile, "2025", "03", "dev")

#### Funcionalidad para obtener el listado de loadrules de un perfil.
# obtener_detalle_loadRules(profile)

#### Funcionalidad para actualizar un load rule de un perfil.
# tps_value = "4"
# listado_page_name = [
#     "test:manu",
#     "test:manu:2",
#     "test:manu:3",
#     f"test:manu:{tps_value}",
# ]
# joinPaginas = "|".join(listado_page_name)
# json_load_rule = {
#     "saveType": "save",
#     "notes": f"Update load rule 2 via API tps{tps_value}",
#     "operationList": [
#         {
#             "op": "replace",
#             "path": f"/loadRules/2",
#             "value": {
#                 "object": "loadRule",
#                 "name": "LR - Unificacion pixel FB",
#                 "status": "active",
#                 "conditions": [
#                     [
#                         {
#                              "operator": "defined",
#                              "value": "",
#                              "variable": "udo.page_name"
#                         },
#                         {
#                             "operator": "regular_expression",
#                             "value": f"^({joinPaginas})$",
#                             "variable": "udo.page_name"
#                         }
#                     ]
#                 ]
#             }
#         }
#     ]
# }
# #print(json.dumps(json_load_rule, indent=4, sort_keys=True))
# actualizar_load_rule(profile, json_load_rule, tps_value)
