"""
Lib Connections
"""
import requests

from common.exceptions import CLIAuthenticationError, CLIConfigurationError, CLIConnectionError, CLIStatusCodeError
from config.settings import HOST, USERNAME, PASSWORD, TIMEOUT


def authorization_header() -> dict:
    """Definir la cabecera para autentificarse en cada solicitud a la API"""
    if HOST == "":
        raise CLIConfigurationError("No se ha definido el host")
    if USERNAME == "":
        raise CLIConfigurationError("No se ha definido el usuario")
    if PASSWORD == "":
        raise CLIConfigurationError("No se ha definido la contraseña")
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(
            f"{HOST}/token",
            data=data,
            headers=headers,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al tratar de autentificar") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al tratar de autentificar: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al tratar de autentificar") from error
    data_json = response.json()
    if not "access_token" in data_json:
        raise CLIAuthenticationError("No se recibio el access_token en la respuesta")
    return {"Authorization": "Bearer " + data_json["access_token"]}
