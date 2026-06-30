"""
Astro commands
"""

import csv
import logging
import os
import subprocess
from pathlib import Path
from typing import Annotated

from rich.console import Console
from typer import Exit, Option, Typer

from pjecz_gob_mx_cli_typer.config.settings import get_settings

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
empunadura = logging.FileHandler("logs/astro.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)

app = Typer(name="astro", help="Astro commands")


@app.command()
def generar(esta_rama: str = ""):
    """Generar archivos para Astro en GENERATED_DIR leyendo RCLONE_REMOTES_CSV"""
    console = Console()
    console.print("Pendiente de implementar la funcionalidad.")
