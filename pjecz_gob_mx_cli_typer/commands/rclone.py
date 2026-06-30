"""
RCLONE commands
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
empunadura = logging.FileHandler("logs/rclone.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)

app = Typer(name="rclone", help="RCLONE commands")


@app.command()
def copiar(
    esta_rama: str = "",
    este_remoto: str = "",
    guardar: Annotated[bool, Option("--guardar", "-g", help="Guardar o simular (si no se usa) la copia")] = False,
):
    """Copiar archivos desde Google Workspace al directorio SOURCES_DIR leyendo RCLONE_REMOTES_CSV"""
    console = Console()
    if guardar:
        msg = "Copiando archivos desde Google Workspace al directorio SOURCES_DIR..."
    else:
        msg = "Simulando la copia de archivos desde Google Workspace al directorio SOURCES_DIR..."
    bitacora.info(msg)
    console.print(msg)

    # Obtener la configuración
    settings = get_settings()
    sources_dir = Path(settings.SOURCES_DIR)
    rclone_remotes_csv = Path(settings.RCLONE_REMOTES_CSV)

    # Leer el archivo rclone-remotes.csv
    ramas_copiadas_contador = 0
    with open(rclone_remotes_csv, newline="", encoding="utf-8") as puntero:
        lector = csv.DictReader(puntero)
        for fila in lector:
            rama = fila["RAMA"]
            rclone_config = fila["RCLONE_CONFIG"]

            # Saltar si se especificó una rama y no coincide
            if esta_rama and rama != esta_rama:
                continue

            # Saltar si se especificó un remoto y no coincide
            if este_remoto and rclone_config != este_remoto:
                continue

            # Definir los parámetros de origen y destino para rclone
            rclone_source = f"{rclone_config}:"
            destination_path = str(sources_dir / rama)

            # Crear el directorio de destino si no existe
            os.makedirs(destination_path, exist_ok=True)

            # Ejecutar el comando rclone copy
            if guardar:
                command = ["rclone", "copy", "--include", "*.md", rclone_source, destination_path]
            else:
                command = ["rclone", "copy", "--include", "*.md", rclone_source, destination_path, "--dry-run"]
            msg = f"Ejecutando: {' '.join(command)}"
            bitacora.info(msg)
            console.print(msg)
            try:
                result = subprocess.run(command, capture_output=True, check=True, text=True)
            except subprocess.CalledProcessError as error:
                msg = f"Error al ejecutar rclone copy para la rama {rama}"
                bitacora.error(msg)
                console.print(f"[yellow]{msg}[/yellow]")
                console.print(error.stderr)
                continue  # Continuar con la siguiente fila en caso de error

            # Si el resultado no es exitoso, mostrar el error
            if result.returncode != 0:
                msg = f"Error al ejecutar rclone copy para la rama {rama}"
                bitacora.error(msg)
                console.print(f"[yellow]{msg}[/yellow]")
                console.print(error.stderr)
                continue  # Continuar con la siguiente fila en caso de error

            # Incrementar el contador de ramas copiadas
            ramas_copiadas_contador += 1

            # Mostrar mensaje de éxito
            msg = f"Archivos copiados exitosamente para la rama {rama}"
            bitacora.info(msg)
            console.print(f"[green]{msg}[/green]")

    # Mensaje final
    if guardar:
        if ramas_copiadas_contador > 0:
            msg = f"Finaliza la copia. Se copiaron {ramas_copiadas_contador} ramas."
            bitacora.info(msg)
            console.print(f"[green]{msg}[/green]")
        else:
            msg = "Finaliza la copia. No se ha copiado ninguna rama."
            bitacora.warning(msg)
            console.print(f"[yellow]{msg}[/yellow]")
    else:
        if ramas_copiadas_contador > 0:
            msg = f"Simulación finalizada. Se pueden copiar {ramas_copiadas_contador} ramas."
            bitacora.info(msg)
            console.print(f"[green]{msg}[/green]")
        else:
            msg = "Simulación finalizada. No se puede copiar ninguna rama."
            bitacora.warning(msg)
            console.print(f"[yellow]{msg}[/yellow]")
