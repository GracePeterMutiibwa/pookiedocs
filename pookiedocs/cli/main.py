import os
import sys
from pathlib import Path

import click

from pookiedocs import __version__


@click.group()
def cli():
    pass


@cli.command("init")
def initProject():
    projectName = click.prompt("Project name")

    docsDir = Path("docs")
    configFile = Path("pookiedocs.config.py")

    if docsDir.exists() or configFile.exists():
        click.echo("Error: docs/ or pookiedocs.config.py already exists in this directory.")
        sys.exit(1)

    try:
        docsDir.mkdir(parents=True)
    except OSError as error:
        click.echo(f"Error: Failed to create docs/ directory: {error}. Check write permissions.")
        sys.exit(1)

    indexContent = f"# {projectName}\n\nWelcome to the {projectName} documentation.\n"

    try:
        (docsDir / "index.md").write_text(indexContent, encoding="utf-8")
    except OSError as error:
        click.echo(f"Error: Failed to write docs/index.md: {error}. Check write permissions.")
        sys.exit(1)

    configContent = (
        "from pookiedocs.config import DocsConfig\n\n"
        f'DOCS = DocsConfig(\n    name="{projectName}",\n)\n'
    )

    try:
        configFile.write_text(configContent, encoding="utf-8")
    except OSError as error:
        click.echo(f"Error: Failed to write pookiedocs.config.py: {error}. Check write permissions.")
        sys.exit(1)

    click.echo("Created docs/index.md")
    click.echo("Created pookiedocs.config.py")
    click.echo("Run: pookiedocs dev")


@cli.command("dev")
@click.option("--host", default="localhost", help="Host to bind the dev server to")
@click.option("--port", default=3000, type=int, help="Port for the dev server")
@click.option("--config", default="pookiedocs.config.py", help="Path to config file")
def devProject(host, port, config):
    """Start the live-reload dev server (for local development)."""
    from pookiedocs.server import devDocs

    try:
        devDocs(host=host, port=port, config_path=config)
    except FileNotFoundError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        click.echo(f"Error starting dev server: {error}")
        sys.exit(1)


@cli.command("serve")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=3000, type=int, help="Port to listen on")
@click.option("--config", default="pookiedocs.config.py", help="Path to config file")
def serveProject(host, port, config):
    """Build and serve the docs (for production / Docker)."""
    from pookiedocs.server import serveDocs

    try:
        serveDocs(host=host, port=port, config_path=config)
    except FileNotFoundError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        click.echo(f"Error starting server: {error}")
        sys.exit(1)


@cli.command("build")
@click.option("--output", default=None, help="Override the outputDir from config")
@click.option("--config", default="pookiedocs.config.py", help="Path to config file")
def buildProject(output, config):
    """Build the static site to outputDir."""
    from pookiedocs.builder import buildSite

    try:
        buildSite(config_path=config, output_override=output)
    except FileNotFoundError as error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        click.echo(f"Error during build: {error}")
        sys.exit(1)


@cli.command("version")
def showVersion():
    click.echo(f"pookiedocs {__version__}")
