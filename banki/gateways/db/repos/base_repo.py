from typing import Callable, ContextManager

from fastapi import Depends
from sqlalchemy.orm import Session

from banki.gateways.db.session import get_session_dep


class BaseRepo:
    _get_session: Callable[[], ContextManager[Session]]

    def __init__(
        self,
        session_getter: Callable[[], ContextManager[Session]] = Depends(get_session_dep),
    ) -> None:
        self._get_session = session_getter
