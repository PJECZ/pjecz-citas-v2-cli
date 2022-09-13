"""
CLI Commnads Cit Dias Disponibles App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_cit_dias_disponibles, get_cit_dia_disponible

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
):
    """Consultar dias disponibles"""
    rich.print("Consultar dias disponibles...")
    try:
        respuesta = get_cit_dias_disponibles(
            limit=limit,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("Fecha")
    for registro in respuesta:
        table.add_row(registro["fecha"])
    console.print(table)


@app.command()
def proximo():
    """Consultar proximo dia hábil"""
    rich.print("Consultar proximo dia hábil...")
    try:
        respuesta = get_cit_dia_disponible()
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(f"Proximo dia hábil: [green]{respuesta['fecha']}[/green]")
