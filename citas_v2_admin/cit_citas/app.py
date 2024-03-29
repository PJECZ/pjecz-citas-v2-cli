"""
CLI Cit Citas App
"""
import csv
from datetime import datetime

import pandas as pd
import rich
import typer

from common.exceptions import CLIAnyError
from common.formats import df_to_table
from config.settings import LIMIT

from .request_api import get_cit_citas, get_cit_citas_agendadas_por_oficina_servicio, get_cit_citas_creados_por_dia, get_cit_citas_creados_por_dia_distrito
from .send_messages import send_agenda, send_agenda_a_usuarios, send_informe_diario

app = typer.Typer()

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)


@app.command()
def consultar(
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    estado: str = None,
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
    guardar: bool = False,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
):
    """Consultar citas"""
    rich.print("Consultar citas...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas(
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            estado=estado,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            limit=limit,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["ID", "Creado", "Oficina", "Inicio", "Nombre", "e-mail", "Servicio", "Estado", "P.C.?", "C.A."]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"cit_citas_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                creado = datetime.strptime(registro["creado"][:18], "%Y-%m-%dT%H:%M:%S")
                inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
                escritor.writerow(
                    [
                        registro["id"],
                        creado.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["oficina_clave"],
                        inicio.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["cit_cliente_nombre"],
                        registro["cit_cliente_email"],
                        registro["cit_servicio_clave"],
                        registro["estado"],
                        "SI" if registro["puede_cancelarse"] else "",
                        registro["codigo_asistencia"],
                    ]
                )

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"][:18], "%Y-%m-%dT%H:%M:%S")
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["oficina_clave"],
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["cit_cliente_nombre"],
            registro["cit_cliente_email"],
            registro["cit_servicio_clave"],
            registro["estado"],
            "SI" if registro["puede_cancelarse"] else "",
            registro["codigo_asistencia"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
    if guardar:
        rich.print(f"Datos guardados en el archivo [blue]{nombre_archivo_csv}[/blue]")


@app.command()
def enviar(
    email: str,
    inicio: str,
    oficina_clave: str,
    limit: int = LIMIT,
    test: bool = True,
):
    """Enviar mensaje con la agenda"""
    rich.print("Enviar mensaje con la agenda...")
    try:
        mensaje = send_agenda(
            email=email,
            inicio=inicio,
            oficina_clave=oficina_clave,
            limit=limit,
            test=test,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(mensaje)


@app.command()
def mostrar_creados_por_dia(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
    guardar: bool = False,
):
    """Mostrar cantidades de citas creadas por dia"""
    rich.print("Mostrar cantidades de citas creadas por dia...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas_creados_por_dia(
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["Creado", "Cantidad"]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"cit_citas_creados_por_dia_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["creado"],
                        registro["cantidad"],
                    ]
                )

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    table.add_column(encabezados[0])
    table.add_column(encabezados[1], justify="right")
    for item in respuesta["items"]:
        table.add_row(item["creado"], str(item["cantidad"]))
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
    if guardar:
        rich.print(f"Datos guardados en el archivo [blue]{nombre_archivo_csv}[/blue]")


@app.command()
def mostrar_creados_por_dia_distrito(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    guardar: bool = False,
):
    """Mostrar cantidades de citas creadas por dia y por distrito"""
    rich.print("Mostrar cantidades de citas creadas por dia y por distrito...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas_creados_por_dia_distrito(
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Convertir datos a pandas dataframe
    df = pd.DataFrame(respuesta["items"])

    # Cambiar el tipo de columna a categoria
    df.creado = df.creado.astype("category")
    df.distrito = df.distrito.astype("category")

    # Crear una tabla pivote
    pivot_table = df.pivot_table(
        index="creado",
        columns="distrito",
        values="cantidad",
        aggfunc="sum",
    )

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"cit_citas_creados_por_dia_distrito_{fecha_hora}.csv"
        pivot_table.to_csv(nombre_archivo_csv)

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Fechas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
    if guardar:
        rich.print(f"Datos guardados en el archivo [blue]{nombre_archivo_csv}[/blue]")


@app.command()
def mostrar_agendadas_por_oficina_servicio(
    inicio: str = None,
    inicio_desde: str = None,
    inicio_hasta: str = None,
    guardar: bool = False,
):
    """Mostrar cantidades de citas agendadas por oficina y servicio"""
    rich.print("Mostrar cantidades de citas agendadas por oficina y servicio...")

    # Solicitar datos
    try:
        respuesta = get_cit_citas_agendadas_por_oficina_servicio(
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Convertir datos a pandas dataframe
    df = pd.DataFrame(respuesta["items"])

    # Cambiar el tipo de columna a categoria
    df.oficina = df.oficina.astype("category")
    df.servicio = df.servicio.astype("category")

    # Crear una tabla pivote
    pivot_table = df.pivot_table(
        index="oficina",
        columns="servicio",
        values="cantidad",
        aggfunc="sum",
    )

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"cit_citas_agendadas_por_oficina_servicio_{fecha_hora}.csv"
        pivot_table.to_csv(nombre_archivo_csv)

    # Mostrar la tabla
    tabla = rich.table.Table(show_lines=False)
    tabla = df_to_table(pivot_table, tabla, "Oficinas")
    console = rich.console.Console()
    console.print(tabla)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] citas")
    if guardar:
        rich.print(f"Datos guardados en el archivo [blue]{nombre_archivo_csv}[/blue]")


@app.command()
def enviar_informe_diario(
    email: str,
    test: bool = True,
):
    """Enviar informe diario"""
    rich.print("Enviar informe diario...")
    try:
        mensaje = send_informe_diario(
            email=email,
            test=test,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(mensaje)


@app.command()
def enviar_agenda_a_usuarios(
    test: bool = True,
):
    """Enviar la agenda de las citas a los usuarios"""
    rich.print("Enviar la agenda de las citas a los usuarios...")
    try:
        mensaje = send_agenda_a_usuarios(
            test=test,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(mensaje)
