"""
CLI Commands Cit Servicios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import BASE_URL, LIMIT, TIMEOUT


def get_cit_servicios(
    authorization_header: dict,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar servicios"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        response = requests.get(
            f"{BASE_URL}/cit_servicios",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar cit_servicios") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar cit_servicios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar cit_servicios") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise CLIResponseError("No se recibio items o total en la respuesta al solicitar cit_servicios")
    return data_json
