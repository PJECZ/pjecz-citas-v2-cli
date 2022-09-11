"""
CLI Cit Clientes Registros App
"""
from datetime import datetime

import rich
import typer

from common.authentication import authorization_header
from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_cit_clientes_registros, get_cit_clientes_registros_cantidades_creados_por_dia

app = typer.Typer()


@app.command()
def consultar(
    apellido_primero: str = None,
    apellido_segundo: str = None,
    curp: str = None,
    email: str = None,
    limit: int = LIMIT,
    nombres: str = None,
    registrado: bool = False,
    offset: int = 0,
):
    """Consultar registros de los clientes"""
    rich.print("Consultar registros de los clientes...")
    try:
        respuesta = get_cit_clientes_registros(
            authorization_header=authorization_header(),
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            email=email,
            limit=limit,
            nombres=nombres,
            offset=offset,
            registrado=registrado,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Nombres", "A. Primero", "A. Segundo", "CURP", "e-mail", "Expiracion", "Mensajes", "Registrado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        expiracion = datetime.strptime(registro["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["nombres"],
            registro["apellido_primero"],
            registro["apellido_segundo"],
            registro["curp"],
            registro["email"],
            expiracion.strftime("%Y-%m-%d %H:%M:%S"),
            str(registro["mensajes_cantidad"]),
            "YA" if bool(registro["ya_registrado"]) else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] registros")


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
):
    """Mostrar cantidades de registros creados por dia"""
    rich.print("Mostrar cantidades de registros creados por dia...")
    try:
        respuesta = get_cit_clientes_registros_cantidades_creados_por_dia(
            authorization_header=authorization_header(),
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table()
    table.add_column("Creado")
    table.add_column("Cantidad", justify="right")
    for creado, cantidad in respuesta["items"].items():
        table.add_row(creado, str(cantidad))
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] registros")
