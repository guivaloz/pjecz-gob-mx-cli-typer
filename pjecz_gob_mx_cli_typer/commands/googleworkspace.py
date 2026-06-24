"""
Google Workspace commands
"""

from rich.console import Console
from rich.table import Table
from typer import Exit, Typer

app = Typer(name="googleworkspace", help="Google Workspace commands")


@app.command()
def copiar():
    """Copiar archivos desde Google Workspace al directorio local"""
    console = Console()
    console.print("Pendiente de implementar la funcionalidad de copiar archivos.")
