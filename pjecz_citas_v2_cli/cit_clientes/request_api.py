"""
CLI Cit Clientes Request API
"""
from datetime import date
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import BASE_URL, LIMIT, TIMEOUT


def get_cit_clientes(
    authorization_header: dict,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
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
    if curp is not None:
        parametros["curp"] = curp
    if email is not None:
        parametros["email"] = email
    if nombres is not None:
        parametros["nombres"] = nombres
    if offset > 0:
        parametros["offset"] = offset
    if telefono is not None:
        parametros["telefono"] = telefono
    try:
        response = requests.get(
            f"{BASE_URL}/cit_clientes",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar cit_clientes: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar cit_clientes") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise CLIResponseError("No se recibio items o total al solicitar cit_clientes")
    return data_json


def get_cit_clientes_creados_por_dia(
    authorization_header: dict,
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
        response = requests.get(
            f"{BASE_URL}/cit_clientes/creados_por_dia",
            headers=authorization_header,
            params=parametros,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar cit_clientes") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar cit_clientes: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar cit_clientes") from error
    data_json = response.json()
    if "items" not in data_json or "total" not in data_json:
        raise CLIResponseError("No se recibio items o total al solicitar cit_clientes")
    return data_json
