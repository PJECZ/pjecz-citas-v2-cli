"""
CLI Usuarios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_usuarios(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    estatus: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
) -> Any:
    """Solicitar usuarios"""
    parametros = {"limit": limit}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if estatus is not None:
        parametros["estatus"] = estatus
    if offset > 0:
        parametros["offset"] = offset
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    try:
        respuesta = requests.get(
            f"{BASE_URL}/usuarios",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar usuarios") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar usuarios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar usuarios") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar usuarios: " + datos["message"])
        raise CLIResponseError("Error al solicitar usuarios")
    return datos["result"]
