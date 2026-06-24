"""
PJECZ GOB MX CLI Typer
"""

from typer import Typer

from pjecz_gob_mx_cli_typer.commands.googleworkspace import app as googleworkspace_app

app = Typer()
app.add_typer(googleworkspace_app, name="googleworkspace")

if __name__ == "__main__":
    app()
