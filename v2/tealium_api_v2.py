import requests
import json
import os
import time


# Archivo para guardar los datos del token
token_file = "tealiumTokenV2.json"
max_retries = 1

# Variables globales
api_key = None
username = None
jwt = None


def guardar_datos():
    with open(token_file, "w") as file:
        json.dump({
            "api_key": api_key,
            "username": username,
            "token": jwt
        }, file)

def cargar_datos():
    global api_key, username, jwt
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            data = json.load(file)
            api_key = data["api_key"]
            username = data["username"]
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