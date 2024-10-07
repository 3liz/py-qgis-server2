import os

from pathlib import Path

import click

PathType = click.Path(
    exists=True,
    readable=True,
    dir_okay=False,
    path_type=Path,
)


@click.group()
def main():
    pass


@main.command('worker')
@click.option(
    "--conf",
    "-C",
    "configpath",
    type=PathType,
    help="Path to configuration file",
)
@click.option(
    "--loglevel",
    "-l",
    type=click.Choice(('error', 'warning', 'info', 'debug')),
    default="info",
    help="Log level",
)
@click.option("--dump", is_flag=True, help="Dump config and exit")
def run_worker(
    configpath: Path,
    loglevel: str,
    dump: bool,
):
    """ Run processes worker
    """
    from .worker.config import CONFIG_ENV_PATH
    if configpath:
        os.environ[CONFIG_ENV_PATH] = str(configpath)

    if dump:
        from pydantic import BaseModel
        from typing_extensions import cast

        from .worker.config import load_configuration
        conf = cast(BaseModel, load_configuration())
        click.echo(conf.model_dump_json(indent=4))
    else:
        from .jobs import app
        app.start_worker(loglevel=loglevel)


@main.command('serve')
@click.option(
    "--conf",
    "-C",
    "configpath",
    type=PathType,
    help="Path to configuration file",
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose mode (trace)")
def run_server(
    configpath: Path,
    verbose: bool,
):
    """ Run server
    """
    from py_qgis_contrib.core import logger

    from .server import load_configuration, serve

    conf = load_configuration(configpath)
    logger.setup_log_handler(
        logger.LogLevel.TRACE if verbose else conf.logging.level,
    )

    serve(conf)


main()
