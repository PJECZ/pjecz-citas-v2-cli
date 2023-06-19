"""
CLI Boletines App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_boletines

encabezados = ["ID", "Envío", "Asunto", "Puntero", "Término"]

app = typer.Typer()


@app.command()
def consultar(
    estado: str = None,
    envio_programado_desde: str = None,
    envio_programado_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar boletines"""
    rich.print("Consultar boletines...")

    # Solicitar datos
    try:
        respuesta = get_boletines(
            estado=estado,
            envio_programado_desde=envio_programado_desde,
            envio_programado_hasta=envio_programado_hasta,
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
        envio_programado_datetime = datetime.fromisoformat(registro["envio_programado"].replace("Z", "+00:00"))
        if registro["termino_programado"] is None:
            termino_programado_datetime = None
        else:
            termino_programado_datetime = datetime.fromisoformat(registro["termino_programado"].replace("Z", "+00:00"))
        table.add_row(
            str(registro["id"]),
            envio_programado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["asunto"],
            str(registro["puntero"]),
            "ND" if termino_programado_datetime is None else termino_programado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] boletines")
