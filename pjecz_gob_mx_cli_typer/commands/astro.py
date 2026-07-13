"""
Astro commands
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from rich.console import Console
from typer import Option, Typer

from pjecz_gob_mx_cli_typer.config.settings import get_settings

METADATA_KEYS = {"Title", "Summary", "Date", "Modify", "Key"}

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
empunadura = logging.FileHandler("logs/astro.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)

app = Typer(name="astro", help="Astro commands")


def parse_metadata(contenido: str) -> tuple[dict[str, str], str]:
    """Parse metadata from first lines and return metadata dict + content without metadata"""
    metadata = {}
    lines = contenido.split("\n")
    idx = 0
    for idx, line in enumerate(lines):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if key in METADATA_KEYS:
                metadata[key] = value.strip()
            else:
                break
        else:
            break
    content_without_metadata = "\n".join(lines[idx:])
    return metadata, content_without_metadata


@app.command()
def generar(
    esta_rama: str = "",
    guardar: Annotated[bool, Option("--guardar", "-g", help="Si no se usa, se simula la generación")] = False,
):
    """Generar archivos para Astro en GENERATED_DIR leyendo RCLONE_REMOTES_CSV"""
    console = Console()
    if guardar:
        msg = "Generando los archivos para Astro en GENERATED_DIR..."
    else:
        msg = "Simulando la generación de los archivos para Astro en GENERATED_DIR..."
    bitacora.info(msg)
    console.print(msg)

    # Obtener la configuración
    settings = get_settings()
    generated_dir = Path(settings.GENERATED_DIR)
    sources_dir = Path(settings.SOURCES_DIR)

    # Inicializar los contadores de archivos generados
    archivos_generados_contador = 0

    # Obtener la lista de archivos en SOURCES_DIR, filtrando solo los archivos con extensión .md
    for archivo_md in sources_dir.glob("**/*.md"):
        if archivo_md.is_file():
            # La ruta relativa del archivo .md con respecto a SOURCES_DIR
            ruta_relativa = archivo_md.relative_to(sources_dir)

            # Saltar si se especifica una rama y la ruta no contiene la rama
            if esta_rama and not ruta_relativa.parts[0].startswith(esta_rama):
                continue

            # Aquí puedes agregar la lógica para procesar cada archivo .md
            console.print(f"Procesando archivo: {ruta_relativa}")

            # Leer el contenido del archivo .md
            with open(archivo_md, "r", encoding="utf-8") as puntero:
                contenido = puntero.read()

                # Parsear metadatos del archivo fuente
                metadata, contenido_limpio = parse_metadata(contenido)

                # Para cada archivo hay que poner en las primeras lineas los metadatos para Astro
                metadatos = []

                # 0. Separador ---
                metadatos.append("---")

                # 1. Que se base en el BaseLayout
                metadatos.append("layout: BaseLayout")

                # 2. Título: usar Title del archivo si existe, si no usar el nombre del archivo
                title = metadata.get("Title", archivo_md.stem)
                metadatos.append(f"title: {title}")

                # 3. Descripción: usar Summary del archivo si existe, si no usar el título
                description = metadata.get("Summary", title)
                metadatos.append(f"description: {description}")

                # 4. Fecha de creación en formato ISO
                created = datetime.fromtimestamp(archivo_md.stat().st_ctime, tz=timezone.utc).isoformat()
                metadatos.append(f"created: {created}")

                # 5. Fecha de modificación en formato ISO
                modified = datetime.fromtimestamp(archivo_md.stat().st_mtime, tz=timezone.utc).isoformat()
                metadatos.append(f"modified: {modified}")

                # 6. Separador ---
                metadatos.append("---")

                # Crear un archivo con el mismo nombre en GENERATED_DIR
                if guardar:
                    archivo_generado = generated_dir / ruta_relativa
                    archivo_generado.parent.mkdir(parents=True, exist_ok=True)
                    with open(archivo_generado, "w", encoding="utf-8") as puntero_generado:
                        puntero_generado.write("\n".join(metadatos) + "\n\n" + contenido_limpio)
                        console.print(f"Archivo generado: {archivo_generado}")

                # Incrementar el contador de archivos generados
                archivos_generados_contador += 1

    # Mensaje final
    if guardar:
        if archivos_generados_contador > 0:
            msg = f"Finaliza la generación de archivos. Se generaron {archivos_generados_contador} archivos."
            bitacora.info(msg)
            console.print(f"[green]{msg}[/green]")
        else:
            msg = "Finaliza la generación de archivos. No se generaron archivos."
            bitacora.info(msg)
            console.print(f"[yellow]{msg}[/yellow]")
    else:
        if archivos_generados_contador > 0:
            msg = f"Simulación finalizada. Se pueden generar {archivos_generados_contador} archivos."
            bitacora.info(msg)
            console.print(f"[green]{msg}[/green]")
        else:
            msg = "Simulación finalizada. No hay archivos para generar."
            bitacora.info(msg)
            console.print(f"[yellow]{msg}[/yellow]")
