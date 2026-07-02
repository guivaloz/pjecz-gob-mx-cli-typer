# pjecz-gob-mx-cli-typer

CLI (Command Line Interface) para construir el nuevo sitio web.

## Estructura del proyecto

- `generated/`: Directorio donde se generarán los archivos para Astro.
- `logs/`: Directorio para almacenar los registros de ejecución del CLI.
- `pjecz_gob_mx_cli_typer/`: Contiene el código fuente del proyecto.
- `sources/`: Directorio para almacenar los archivos fuente que se utilizarán en la construcción del sitio web.

## Uso después de la instalación

Cargar el archivo `.bashrc`

```bash
source .bashrc
```

Ejecutar el CLI con la opción `--help` para ver las opciones disponibles

```bash
cli --help
```

## Instalación

Crear un entorno virtual con Python 3.14

```bash
python3.14 -m venv .venv
```

Activar el entorno virtual

```bash
source .venv/bin/activate  # En Linux o macOS
.venv\Scripts\activate  # En Windows
```

Si no lo tiene instalado, instalar `uv`

```bash
pip install uv
```

Instalar las dependencias por medio de `uv`

```bash
uv sync
```

Copiar el archivo de ejemplo de configuración como `.env`

```bash
cp .env.example .env
```

Editar el archivo `.env` para configurar las variables de entorno según sea necesario.

```bash
nano .env
```

Crear un archivo bash para cargar las variables de entorno y entrar al entorno virtual

```bash
nano .bashrc
```

Con este contenido

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet PJECZ gob mx CLI Typer
else
    echo "== PJECZ gob mx CLI Typer"
fi
echo

if [ -f .env ]
then
    echo "-- Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_PORT: ${DB_PORT}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   GENERATED_DIR: ${GENERATED_DIR}"
    echo "   RCLONE_REMOTES_CSV: ${RCLONE_REMOTES_CSV}"
    echo "   SQLALCHEMY_DATABASE_URI: ${SQLALCHEMY_DATABASE_URI}"
    echo "   SOURCES_DIR: ${SOURCES_DIR}"
    echo "   TZ: ${TZ}"
    echo
    export PGHOST=$DB_HOST
    export PGPORT=$DB_PORT
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    alias cli="uv run ${PWD}/pjecz_gob_mx_cli_typer/app.py"
    echo "-- Ejecutar el CLI"
    echo "   cli --help"
    echo
fi
```
