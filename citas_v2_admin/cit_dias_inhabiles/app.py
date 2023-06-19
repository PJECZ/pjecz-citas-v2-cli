"""
CLI Citas Dias Inhabiles App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_cit_dias_inhabiles

encabezados = ["ID", "Fecha", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar dias inhabiles"""
    rich.print("Consultar dias inhabiles...")

    # Solicitar datos
    try:
        respuesta = get_cit_dias_inhabiles(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["fecha"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] dias inhabiles")
