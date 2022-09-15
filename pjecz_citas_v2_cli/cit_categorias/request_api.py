"""
CLI Cit Categorias Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_cit_categorias(
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar cit_categorias"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_categorias",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar categorias") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar categorias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar categorias") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar categorias: " + datos["message"])
        raise CLIResponseError("Error al solicitar categorias")
    return datos["result"]
