"""
The CLI module for the study version.

This module defines the following CLI commands:

- antares-study-version show: display the details of a study in human-readable format (name, version, creation date, etc.)
- antares-study-version create: create a new study.
"""

from pathlib import Path

import click

from antares.study.version import StudyVersion
from antares.study.version.__about__ import __date__, __version__
from antares.study.version.create_app import CreateApp, available_versions
from antares.study.version.exceptions import ApplicationError
from antares.study.version.show_app import ShowApp
from antares.study.version.upgrade_app import UpgradeApp

INTERRUPTED_BY_THE_USER = "Operation interrupted by the user."


@click.group(context_settings={"max_content_width": 120})
@click.version_option(__version__, message=f"v{__version__} ({__date__})")
def cli() -> None:
    """
    Main entrypoint for the CLI application.
    """


@cli.command()
@click.argument(
    "study_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
def show(study_dir: str) -> None:
    """
    Display the details of a study in human-readable format.

    STUDY_DIR: The directory containing the study.
    """
    try:
        app = ShowApp(Path(study_dir))
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

    try:
        app()
    except ApplicationError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except KeyboardInterrupt:
        click.echo(INTERRUPTED_BY_THE_USER, err=True)
        raise click.Abort()


def _display_available_versions(ctx: click.Context, _param: click.Option, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Available versions: {', '.join(available_versions())}")
    ctx.exit()


@cli.command()
@click.argument(
    "study_dir",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "-c",
    "--caption",
    default="New Study",
    help="Caption of the study",
    show_default=True,
)
@click.option(
    "-v",
    "--version",
    default=available_versions()[-1],
    help="Version of the study to create",
    show_default=True,
    type=click.Choice(available_versions()),
)
@click.option(
    "-a",
    "--author",
    default="Anonymous",
    help="Author of the study",
    show_default=True,
)
@click.option(
    "--versions",
    is_flag=True,
    callback=_display_available_versions,
    expose_value=False,
    is_eager=True,
    help="Display all available upgrade versions and quit.",
)
def create(study_dir: str, caption: str, version: str, author: str) -> None:
    """
    Create a new study in the specified directory.

    STUDY_DIR: The directory where the study will be created.
    """
    try:
        app = CreateApp(Path(study_dir), caption=caption, version=StudyVersion.parse(version), author=author)
    except (ValueError, FileExistsError) as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

    try:
        app()
    except ApplicationError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except KeyboardInterrupt:
        click.echo(INTERRUPTED_BY_THE_USER, err=True)
        raise click.Abort()


@cli.command()
@click.argument(
    "study_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
)
@click.option(
    "-v",
    "--version",
    default=available_versions()[-1],
    help="Version of the study to create",
    show_default=True,
    type=click.Choice(available_versions()),
)
def upgrade(study_dir: str, version: str) -> None:
    """
    Upgrade a study to a new version.

    STUDY_DIR: The directory containing the study to upgrade.
    """
    try:
        app = UpgradeApp(Path(study_dir), version=StudyVersion.parse(version))
    except (ValueError, FileNotFoundError) as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

    try:
        app()
    except ApplicationError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except KeyboardInterrupt:
        click.echo(INTERRUPTED_BY_THE_USER, err=True)
        raise click.Abort()
