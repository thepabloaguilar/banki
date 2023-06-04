from contextlib import contextmanager
from typing import Callable, ContextManager, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from banki.configuration import settings

_db_engine = create_engine(
    settings.SQLALCHEMY_DB_URI,
    poolclass=NullPool,
    echo=settings.SQLALCHEMY_ECHO,
)

session = scoped_session(sessionmaker(
    bind=_db_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
))


@contextmanager
def get_session() -> Iterator[Session]:
    new_session = session()

    try:
        yield new_session
    finally:
        new_session.rollback()
        new_session.close()


def get_session_dep() -> Callable[[], ContextManager[Session]]:
    return get_session
