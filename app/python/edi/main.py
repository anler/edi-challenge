import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, List

import typer
from domain import use_case
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = typer.Typer()
state = {"verbose": False, "loglevel": logging.INFO}
log = logging.getLogger()


@app.command(name="import", help="Import EDI files")
def file_import(
    db_url: Annotated[str, typer.Argument(help="Database URL")],
    files: List[Annotated[Path, typer.Argument(help="Path to EDI 867 files")]],
) -> None:
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    cmd = use_case.ImportTexasEdi867_02(Session=Session, delim="~")
    for file in files:
        cmd.execute(open(file))


@app.command(name="create-db", help="Create the initial database file")
def create_db(db_url: Annotated[str, typer.Argument(help="Database URL")]) -> None:
    engine = create_engine(db_url)
    cmd = use_case.CreateDb(engine)
    cmd.execute()


class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


@app.callback()
def main(
    verbose: Annotated[bool, typer.Option(..., "-v", "--verbose", envvar="VERBOSE", help="Verbose output")] = False,
    loglevel: Annotated[
        LogLevel,
        typer.Option(
            ...,
            "-l",
            "--loglevel",
            envvar="LOG_LEVEL",
            help="Log level",
        ),
    ] = LogLevel.error,
) -> None:
    level = getattr(logging, loglevel.upper(), logging.INFO)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=level,
    )
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        logger.setLevel(level)

    log.debug("Logging configured")

    state["verbose"] = verbose
    state["loglevel"] = level


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        if state["verbose"]:
            log.exception(e)
        else:
            log.error("%s: %s", type(e).__name__, e)
        sys.exit(1)
