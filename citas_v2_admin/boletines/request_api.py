"""
CLI Boletines Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_boletines(
    estado: str = None,
    envio_programado_desde: str = None,
    envio_programado_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar boletines"""
    parametros = {"limit": limit}
    if estado is not None:
        parametros["estado"] = estado
    if envio_programado_desde is not None:
        parametros["envio_programado_desde"] = envio_programado_desde
    if envio_programado_hasta is not None:
        parametros["envio_programado_hasta"] = envio_programado_hasta
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/boletines",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar boletines") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar boletines: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar boletines") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar boletines: " + datos["message"])
        raise CLIResponseError("Error al solicitar boletines")
    return datos["result"]
