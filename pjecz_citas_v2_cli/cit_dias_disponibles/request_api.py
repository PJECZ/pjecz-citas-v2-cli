"""
CLI Cit Dias Disponibles Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_cit_dias_disponibles(
    size: int = LIMIT,
) -> Any:
    """Solicitar dias disponibles, entrega un listado de fechas"""
    parametros = {"size": size}
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_dias_disponibles",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar dias disponibles") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar dias disponibles: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar dias disponibles") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar dias disponibles: " + datos["message"])
        raise CLIResponseError("Error al solicitar dias disponibles")
    return datos["result"]


def get_cit_dia_disponible() -> Any:
    """Solicitar el proximo dia disponible, por ejemplo, si hoy es viernes y el lunes es dia inhabil, entrega el martes"""
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_dias_disponibles/proximo",
            headers={"X-Api-Key": API_KEY},
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar el proximo dia disponible") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar el proximo dia disponible: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar el proximo dia disponible") from error
    datos = respuesta.json()
    if "fecha" not in datos:
        raise CLIResponseError("Error al solicitar el proximo dia disponible")
    return datos["fecha"]
