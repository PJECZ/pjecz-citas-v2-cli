"""
CLI Enc Servicios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_enc_servicios(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    estado: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
) -> Any:
    """Solicitar encuestas de servicios"""
    parametros = {"limit": limit}
    if cit_cliente_id is not None:
        parametros["cit_cliente_id"] = cit_cliente_id
    if cit_cliente_email is not None:
        parametros["cit_cliente_email"] = cit_cliente_email
    if estado is not None:
        parametros["estado"] = estado
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/enc_servicios",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar encuestas de servicios") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar encuestas de servicios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar encuestas de servicios") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar encuestas de servicios: " + datos["message"])
        raise CLIResponseError("Error al solicitar encuestas de servicios")
    return datos["result"]
