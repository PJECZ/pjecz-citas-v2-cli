"""
CLI Oficinas App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_oficinas

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    domicilio_id: int = None,
    estatus: str = None,
    guardar: bool = False,
    limit: int = LIMIT,
    puede_agendar_citas: bool = True,
    offset: int = 0,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")

    # Solicitar datos
    try:
        respuesta = get_oficinas(
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            estatus=estatus,
            limit=limit,
            puede_agendar_citas=puede_agendar_citas,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["ID", "Clave", "Distrito", "Descripcion", "P.A.C.", "Apertura", "Cierre", "L.P."]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"oficinas_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["clave"],
                        registro["distrito_nombre_corto"],
                        registro["descripcion_corta"],
                        "SI" if bool(registro["puede_agendar_citas"]) else "",
                        registro["apertura"],
                        registro["cierre"],
                        str(registro["limite_personas"]),
                    ]
                )
        rich.print(f"Datos guardados en el archivo {nombre_archivo_csv}")

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["descripcion_corta"],
            "SI" if bool(registro["puede_agendar_citas"]) else "",
            registro["apertura"],
            registro["cierre"],
            str(registro["limite_personas"]),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")
