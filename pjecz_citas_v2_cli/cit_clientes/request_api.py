"""
CLI Cit Clientes Request API
"""
from datetime import date
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_cit_clientes(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    autoriza_mensajes: bool = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    limit: int = LIMIT,
    nombres: str = None,
    offset: int = 0,
    telefono: str = None,
) -> Any:
    """Solicitar el listado de clientes"""
    parametros = {"limit": limit}
    if apellido_primero is not None:
        parametros["apellido_primero"] = apellido_primero
    if apellido_segundo is not None:
        parametros["apellido_segundo"] = apellido_segundo
    if autoriza_mensajes is not None:
        parametros["autoriza_mensajes"] = autoriza_mensajes
    if curp is not None:
        parametros["curp"] = curp
    if email is not None:
        parametros["email"] = email
    if enviar_boletin is not None:
        parametros["enviar_boletin"] = enviar_boletin
    if nombres is not None:
        parametros["nombres"] = nombres
    if offset > 0:
        parametros["offset"] = offset
    if telefono is not None:
        parametros["telefono"] = telefono
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_clientes",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar clientes") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar clientes: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar clientes") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar clientes: " + datos["message"])
        raise CLIResponseError("Error al solicitar clientes")
    return datos["result"]


def get_cit_clientes_creados_por_dia(
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
) -> Any:
    """Solicitar cantidades de clientes creadas por dia"""
    parametros = {}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    try:
        respuesta = requests.get(
            f"{BASE_URL}/cit_clientes/creados_por_dia",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar clientes") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar clientes: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar clientes") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar clientes: " + datos["message"])
        raise CLIResponseError("Error al solicitar clientes")
    return datos["result"]
