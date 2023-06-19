"""
CLI Cit Clientes Recuperaciones Request API
"""
from datetime import date
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_cit_clientes_recuperaciones(
    email: str = None,
    limit: int = LIMIT,
    recuperado: bool = None,
    offset: int = 0,
) -> Any:
    """Solicitar el listado de recuperaciones"""
    parametros = {"limit": limit}
    if email is not None:
        parametros["cit_cliente_email"] = email
    if recuperado is not None:
        parametros["ya_recuperado"] = recuperado
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_clientes_recuperaciones",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar recuperaciones") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar recuperaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar recuperaciones") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar recuperaciones: " + datos["message"])
        raise CLIResponseError("Error al solicitar recuperaciones")
    return datos["result"]


def get_cit_clientes_recuperaciones_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Solicitar cantidades de recuperaciones creadas por dia"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_clientes_recuperaciones/creados_por_dia",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar recuperaciones") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar recuperaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar recuperaciones") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar recuperaciones: " + datos["message"])
        raise CLIResponseError("Error al solicitar recuperaciones")
    return datos["result"]
