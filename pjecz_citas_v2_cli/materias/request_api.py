"""
CLI Materias Request API
"""
from typing import Any

import requests

from common.exceptions import CLIStatusCodeError, CLIConnectionError, CLIResponseError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_materias(
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar materias"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/materias",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar materias") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar materias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar materias") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise CLIResponseError("No se recibio items o total en la respuesta al solicitar materias")
    return data_json
