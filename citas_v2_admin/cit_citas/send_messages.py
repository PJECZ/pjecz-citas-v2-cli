"""
CLI Cit Citas Send Messages
"""
from datetime import datetime, timedelta
import locale
from pathlib import Path
from typing import Any

from dominate import document
from dominate.tags import div
from dominate.util import raw
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate

from common.exceptions import CLIConfigurationError, CLINoDataWarning
from config.settings import LIMIT, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL

from .request_api import get_cit_citas, get_cit_citas_agendadas_por_oficina_servicio, get_cit_citas_creados_por_dia
from ..cit_dias_disponibles.request_api import get_cit_dia_disponible
from ..oficinas.request_api import get_oficinas
from ..usuarios.request_api import get_usuarios

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)

# Region
locale.setlocale(locale.LC_TIME, "es_MX.utf8")


def send_agenda(
    email: str,
    inicio: str,
    oficina_clave: str,
    limit: int = LIMIT,
    test: bool = True,
) -> Any:
    """Enviar agenda"""

    # Validar variables de entorno de SendGrid
    if not test and SENDGRID_API_KEY == "":
        raise CLIConfigurationError("Falta SENDGRID_API_KEY")
    if not test and SENDGRID_FROM_EMAIL == "":
        raise CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")

    # Solicitar citas
    respuesta = get_cit_citas(
        inicio=inicio,
        limit=limit,
        oficina_clave=oficina_clave,
    )

    # Si no hay datos CLINoDataWarning
    if respuesta["total"] == 0:
        raise CLINoDataWarning("No hay citas para enviar")

    # Convertir datos a tabla HTML
    headers = ["ID", "Hora", "Nombre", "Servicio", "Notas"]
    rows = []
    for item in respuesta["items"]:
        inicio = datetime.strptime(item["inicio"], "%Y-%m-%dT%H:%M:%S")
        rows.append(
            [
                item["id"],
                inicio.strftime("%H:%M"),
                item["cit_cliente_nombre"],
                item["cit_servicio_clave"],
                item["notas"],
            ]
        )
    table_html = tabulate(rows, headers=headers, tablefmt="html")
    table_html = table_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    table_html = table_html.replace('<td style="', '<td style="padding: 4px;')
    table_html = table_html.replace("<td>", '<td style="padding: 4px;">')

    # Crear mensaje
    subject = f"Citas de la oficina {oficina_clave} para la fecha {inicio}"
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<style> td {border:2px black solid !important} </style>")
    contenidos.append("<h1>PJECZ Citas V2</h1>")
    contenidos.append(f"<h2>{subject}</h2>")
    contenidos.append(table_html)
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

    # Si NO es una prueba, enviar mensaje
    if test is False:
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDGRID_FROM_EMAIL)
        to_email = To(email)
        content = Content("text/html", "<br>".join(contenidos))
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )
        sendgrid_client.client.mail.send.post(request_body=mail.get())
        return f"Mensaje enviado a [blue]{email}[/blue] con [green]{subject}[/green]"

    # Es una prueba, se va a guardar en un archivo
    with document(title=subject) as doc:
        for contenido in contenidos:
            div(raw(contenido))
    archivo = "enviar.html"
    ruta = Path(archivo)
    with open(ruta, "w", encoding="utf-8") as puntero:
        puntero.write(doc.render())
    return f"Se guardo el mensaje en [blue]{archivo}[/blue] con [green]{subject}[/green] porque es una prueba"


def send_agenda_a_usuarios(
    test: bool = True,
) -> Any:
    """Enviar la agenda de su oficina a cada usuario"""

    # Validar variables de entorno de SendGrid
    if not test and SENDGRID_API_KEY == "":
        raise CLIConfigurationError("Falta SENDGRID_API_KEY")
    if not test and SENDGRID_FROM_EMAIL == "":
        raise CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")

    # Obtener el proximo dia habil
    proximo_dia_habil = get_cit_dia_disponible()

    # Obtener las oficinas que pueden agendar citas
    oficinas = get_oficinas(
        estatus="A",
        limit=LIMIT,
        puede_agendar_citas=True,
    )

    # Inicializar el listado de mensajes finales
    mensajes_finales = []

    # Bucle por las oficinas
    for oficina in oficinas["items"]:

        # Obtener la agenda de las citas de la oficina
        citas = get_cit_citas(
            limit=LIMIT,
            inicio=proximo_dia_habil,
            oficina_id=oficina["id"],
        )

        # Si no hay citas, continuar
        if citas["total"] == 0:
            continue

        # Obtener los usuarios de la oficina
        usuarios = get_usuarios(
            estatus="A",
            limit=LIMIT,
            oficina_id=oficina["id"],
        )

        # Si no hay usuarios, continuar
        if usuarios["total"] == 0:
            continue

        # Juntar las direcciones de correo electronico de los usuarios
        usuarios_emails_str = ", ".join([usuario["email"] for usuario in usuarios["items"]])

        # Crear mensaje
        subject = f"Citas de la oficina {oficina['descripcion_corta']} para {proximo_dia_habil}"
        elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
        contenidos = []
        contenidos.append("<style> td {border:2px black solid !important} </style>")
        contenidos.append("<h1>PJECZ Citas V2</h1>")
        contenidos.append(f"<h2>{subject}</h2>")
        headers = ["Hora", "Nombre", "Servicio", "Notas"]
        rows = []
        for item in citas["items"]:
            inicio = datetime.strptime(item["inicio"], "%Y-%m-%dT%H:%M:%S")
            rows.append(
                [
                    inicio.strftime("%H:%M"),
                    item["cit_cliente_nombre"],
                    item["cit_servicio_clave"],
                    item["notas"],
                ]
            )
        table_html = tabulate(rows, headers=headers, tablefmt="html")
        table_html = table_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
        table_html = table_html.replace('<td style="', '<td style="padding: 4px;')
        table_html = table_html.replace("<td>", '<td style="padding: 4px;">')
        contenidos.append(table_html)
        contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
        contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

        # Si NO es una prueba, enviar mensaje
        if test is False:
            sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
            mail = Mail(
                from_email=Email(SENDGRID_FROM_EMAIL),
                to_emails=[usuario["email"] for usuario in usuarios["items"]],
                subject=subject,
                html_content=Content("text/html", "<br>".join(contenidos)),
            )
            sendgrid_client.client.mail.send.post(request_body=mail.get())
            mensajes_finales.append(f"Mensaje enviado a [blue]{usuarios_emails_str}[/blue] con [green]{subject}[/green]")

        # Es una prueba, se va a guardar en un archivo
        with document(title=subject) as doc:
            for contenido in contenidos:
                div(raw(contenido))
        archivo = f"agenda_a_usuarios-{oficina['clave']}.html"
        ruta = Path(archivo)
        with open(ruta, "w", encoding="utf-8") as puntero:
            puntero.write(doc.render())
        mensajes_finales.append(f"Se guardo el mensaje en [blue]{archivo}[/blue] con [green]{subject}[/green] porque es una prueba")

    # Entregar mensajes finales
    return "\n".join(mensajes_finales)


def send_informe_diario(
    email: str,
    test: bool = True,
) -> Any:
    """Enviar Informe Diario"""

    # Validar variables de entorno de SendGrid
    if not test and SENDGRID_API_KEY == "":
        raise CLIConfigurationError("Falta SENDGRID_API_KEY")
    if not test and SENDGRID_FROM_EMAIL == "":
        raise CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")

    # Definir la fecha de hoy y la de ayer
    hoy = datetime.now().strftime("%Y-%m-%d")
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    hace_siete_dias = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Bucle por los distritos

    # Solicitar citas agendadas por oficina y servicio para hoy
    ccaos_respuesta = get_cit_citas_agendadas_por_oficina_servicio(
        inicio=hoy,
    )

    # Omitir si no hay datos

    # Convertir datos a pandas dataframe
    ccaos_df = pd.DataFrame(ccaos_respuesta["items"])

    # Cambiar el tipo de las columnas a categoria
    ccaos_df.oficina = ccaos_df.oficina.astype("category")
    ccaos_df.servicio = ccaos_df.servicio.astype("category")

    # Crear una tabla pivote
    ccaos_pt = ccaos_df.pivot_table(
        index="oficina",
        columns="servicio",
        values="cantidad",
        aggfunc="sum",
    )

    # Convertir la tabla pivote a una tabla HTML
    ccaos_table_html = tabulate(ccaos_pt, headers="keys", tablefmt="html")
    ccaos_table_html = ccaos_table_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    ccaos_table_html = ccaos_table_html.replace('<td style="', '<td style="padding: 4px;')
    ccaos_table_html = ccaos_table_html.replace("<td>", '<td style="padding: 4px;">')

    # Definir el titulo de la tabla
    ccaos_title = f"{ccaos_respuesta['total']} citas agendadas por oficina y servicio en {hoy}"

    # Solicitar las cantidades de citas creadas por dia
    cccd_respuesta = get_cit_citas_creados_por_dia(
        creado_desde=hace_siete_dias,
        creado_hasta=ayer,
    )

    # Pasar items a listado de fechas, cantidades
    cccd_datos = []
    for item in cccd_respuesta["items"]:
        cccd_datos.append([item["creado"], item["cantidad"]])

    # Convertir el dataframe a una tabla HTML
    cccd_table_html = tabulate(cccd_datos, headers=["Fecha", "Cantidad"], tablefmt="html")
    cccd_table_html = cccd_table_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    cccd_table_html = cccd_table_html.replace('<td style="', '<td style="padding: 4px;')
    cccd_table_html = cccd_table_html.replace("<td>", '<td style="padding: 4px;">')

    # Definir el titulo de la tabla
    cccd_title = f"{cccd_respuesta['total']} citas creadas por los clientes en los siguientes dias"

    # Crear mensaje
    subject = f"Citas Informe del {hoy}"
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<style> td {border:2px black solid !important} </style>")
    contenidos.append("<h1>PJECZ Citas V2</h1>")
    contenidos.append(f"<h2>{ccaos_title}</h2>{ccaos_table_html}")
    contenidos.append(f"<h2>{cccd_title}</h2>{cccd_table_html}")
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

    # Si NO es una prueba, enviar mensaje
    if test is False:
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDGRID_FROM_EMAIL)
        to_email = To(email)
        content = Content("text/html", "<br>".join(contenidos))
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )
        sendgrid_client.client.mail.send.post(request_body=mail.get())
        return f"Mensaje enviado a [blue]{email}[/blue] con [green]{subject}[/green]"

    # Es una prueba, se va a guardar en un archivo
    with document(title=subject) as doc:
        for contenido in contenidos:
            div(raw(contenido))
    archivo = "informe-diario.html"
    ruta = Path(archivo)
    with open(ruta, "w", encoding="utf-8") as puntero:
        puntero.write(doc.render())
    return f"Se guardo el mensaje en [blue]{archivo}[/blue] con [green]{subject}[/green] porque es una prueba"
