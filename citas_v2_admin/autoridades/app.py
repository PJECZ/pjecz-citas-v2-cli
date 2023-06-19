"""
CLI Usuarios App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_autoridades

app = typer.Typer()


@app.command()
def consultar(
    estatus: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar autoridades"""
    rich.print("Consultar autoridades...")
    try:
        respuesta = get_autoridades(
            estatus=estatus,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Distrito", "Descripcion corta", "Materia", "E.J.", "E.N.", "O.J.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["descripcion_corta"],
            registro["materia_nombre"],
            "SI" if bool(registro["es_jurisdiccional"]) else "",
            "SI" if bool(registro["es_notaria"]) else "",
            registro["organo_jurisdiccional"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades")
