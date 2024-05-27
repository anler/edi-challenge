from typing import Generator

import pytest
from sqlalchemy import Engine, create_engine, orm

from domain.model import Base


@pytest.fixture
def engine() -> Engine:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine: Engine) -> Generator[orm.Session, None, None]:
    with orm.Session(bind=engine) as session:
        session.begin_nested()
        yield session
        session.rollback()


@pytest.fixture
def Session(engine: Engine) -> Generator[orm.sessionmaker[orm.Session], None, None]:
    with engine.begin() as tx:
        try:
            yield orm.sessionmaker(bind=engine)
        finally:
            tx.rollback()
