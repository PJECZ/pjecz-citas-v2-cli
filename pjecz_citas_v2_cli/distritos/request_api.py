"""
CLI Distritos Request API
"""
from typing import Any

import requests

from common.exceptions import CLIStatusCodeError, CLIConnectionError, CLIResponseError
from config.settings import BASE_URL, LIMIT, TIMEOUT


def get_distritos(
    authorization_header: dict,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar distritos"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/distritos",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar distritos") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar distritos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar distritos") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise CLIResponseError("No se recibio items o total en la respuesta al solicitar distritos")
    return data_json
