"""
Command Line Interface
"""
import typer

from citas_v2_admin.autoridades.app import app as autoridades_app
from citas_v2_admin.boletines.app import app as boletines_app
from citas_v2_admin.cit_categorias.app import app as cit_categorias_app
from citas_v2_admin.cit_citas.app import app as cit_citas_app
from citas_v2_admin.cit_clientes.app import app as cit_clientes_app
from citas_v2_admin.cit_clientes_recuperaciones.app import app as cit_clientes_recuperaciones_app
from citas_v2_admin.cit_clientes_registros.app import app as cit_clientes_registros_app
from citas_v2_admin.cit_dias_disponibles.app import app as cit_dias_disponibles_app
from citas_v2_admin.cit_dias_inhabiles.app import app as cit_dias_inhabiles_app
from citas_v2_admin.cit_servicios.app import app as cit_servicios_app
from citas_v2_admin.distritos.app import app as distritos_app
from citas_v2_admin.enc_servicios.app import app as enc_servicios_app
from citas_v2_admin.enc_sistemas.app import app as enc_sistemas_app
from citas_v2_admin.materias.app import app as materias_app
from citas_v2_admin.oficinas.app import app as oficinas_app
from citas_v2_admin.roles.app import app as roles_app
from citas_v2_admin.usuarios.app import app as usuarios_app

app = typer.Typer()
app.add_typer(autoridades_app, name="autoridades")
app.add_typer(boletines_app, name="boletines")
app.add_typer(cit_categorias_app, name="cit_categorias")
app.add_typer(cit_citas_app, name="cit_citas")
app.add_typer(cit_clientes_app, name="cit_clientes")
app.add_typer(cit_clientes_recuperaciones_app, name="cit_clientes_recuperaciones")
app.add_typer(cit_clientes_registros_app, name="cit_clientes_registros")
app.add_typer(cit_dias_disponibles_app, name="cit_dias_disponibles")
app.add_typer(cit_dias_inhabiles_app, name="cit_dias_inhabiles")
app.add_typer(cit_servicios_app, name="cit_servicios")
app.add_typer(distritos_app, name="distritos")
app.add_typer(enc_servicios_app, name="enc_servicios")
app.add_typer(enc_sistemas_app, name="enc_sistemas")
app.add_typer(materias_app, name="materias")
app.add_typer(oficinas_app, name="oficinas")
app.add_typer(roles_app, name="roles")
app.add_typer(usuarios_app, name="usuarios")

if __name__ == "__main__":
    app()
