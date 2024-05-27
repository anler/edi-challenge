import logging
from dataclasses import dataclass
from typing import Iterable

from edi867_02.parser import Delim, TransactionParser
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from domain.repository import import_segments

from . import model

log = logging.getLogger(__name__)


@dataclass
class ImportTexasEdi867_02:
    Session: sessionmaker[Session]
    delim: Delim = "~"

    def execute(self, lines: Iterable[str]) -> None:
        parser = TransactionParser()
        line_iterator = iter(lines)
        while True:
            try:
                transaction = parser.parse(line_iterator)
                with self.Session.begin() as session:
                    import_segments(session, transaction)
            except StopIteration:
                break
            except Exception as e:
                log.error("Skipping transaction due to an error %s", e)


@dataclass
class CreateDb:
    engine: Engine

    def execute(self) -> None:
        model.Base.metadata.create_all(self.engine)
