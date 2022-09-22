"""
CLI Usuarios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_autoridades(
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar autoridades"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/autoridades",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar autoridades") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar autoridades: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar autoridades") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar autoridades: " + datos["message"])
        raise CLIResponseError("Error al solicitar autoridades")
    return datos["result"]
