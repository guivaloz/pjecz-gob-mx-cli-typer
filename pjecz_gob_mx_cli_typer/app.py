"""
PJECZ GOB MX CLI Typer
"""

from typer import Typer

from pjecz_gob_mx_cli_typer.commands.astro import app as astro_app
from pjecz_gob_mx_cli_typer.commands.rclone import app as rclone_app

app = Typer()
app.add_typer(astro_app, name="astro")
app.add_typer(rclone_app, name="rclone")

if __name__ == "__main__":
    app()
