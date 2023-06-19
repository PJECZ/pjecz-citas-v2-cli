"""
CLI Enc Sistemas App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_enc_sistemas

app = typer.Typer()


@app.command()
def consultar(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    estado: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar encuestas de sistemas"""
    rich.print("Consultar encuestas de sistemas...")

    # Solicitar datos
    try:
        respuesta = get_enc_sistemas(
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            estado=estado,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "e-mail", "Nombre", "R1", "R2", "R3", "Estado")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_email"],
            registro["cit_cliente_nombre"],
            "" if registro["respuesta_01"] is None else str(registro["respuesta_01"]),
            "" if registro["respuesta_02"] is None else str(registro["respuesta_02"]),
            "" if registro["respuesta_03"] is None else str(registro["respuesta_03"]),
            registro["estado"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] encuestas de servicios")
