# Extracted from:
#   https://docs.sqlalchemy.org/en/14/core/compiler.html#utc-timestamp-function

from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):  # type: ignore  # noqa: N801
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')  # type: ignore[no-untyped-call]
def pg_utcnow(element: utcnow, compile: Any, **kwargs: Any) -> str:  # noqa: WPS125
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
