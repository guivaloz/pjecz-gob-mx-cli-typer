# AGENTS.md

## Overview

CLI tool (Typer) for building the PJECZ judiciary website. Copies markdown from Google Drive via rclone, then generates Astro-ready markdown with frontmatter. All UI text and variable names are in Spanish.

## Commands

```bash
uv sync                              # install dependencies
uv run pjecz_gob_mx_cli_typer/app.py --help   # run CLI
uv run python main.py                # alternative entrypoint

# Subcommands (dry-run by default; add --guardar to write)
cli rclone copiar --guardar          # copy .md files from Google Drive to sources/
cli astro generar --guardar          # generate Astro markdown into generated/
```

## Tooling

- **Formatter:** black (line-length 128)
- **Import sort:** isort (line-length 128, profile "black")
- **Type checker:** basedpyright (basic mode, Python 3.14)
- **Linter:** ruff (line-length 128, ignores F821)
- **No test suite** — no pytest in deps, no tests directory

Run formatters/linters with `uv run`:
```bash
uv run black .
uv run isort .
uv run basedpyright
uv run ruff check .
```

## Architecture

- `pjecz_gob_mx_cli_typer/app.py` — Typer app, registers subcommand groups
- `commands/astro.py` — reads `sources/`, writes frontmatter+content to `generated/`
- `commands/rclone.py` — runs `rclone copy` per row in `rclone-remotes.csv`
- `config/settings.py` — pydantic-settings, loads from `.env`
- `rclone-remotes.csv` — maps section names to rclone remote configs and Drive IDs

## Gotchas

- `.env` is required — copy from `.env.example`. Settings include DB creds, directory paths, and `RCLONE_REMOTES_CSV`.
- `PYTHONPATH` must be set to repo root (the `.bashrc` template does this).
- `sources/` and `generated/` are gitignored — they live outside version control.
- `.gitignore` has stale merge conflict markers (lines 230-243); don't be surprised by duplicates.
- `rclone` must be installed and configured with Google Workspace remotes for `rclone copiar` to work.
- Logging goes to `logs/astro.log` and `logs/rclone.log`, not stdout.
- `rclone.py:92` references `error.stderr` but `error` may be unbound if `subprocess.run` succeeded — existing bug.
