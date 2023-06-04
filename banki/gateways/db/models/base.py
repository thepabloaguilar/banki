from datetime import datetime
from decimal import Decimal
from typing import Annotated

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, as_declarative, mapped_column, registry

from banki.gateways.db.functions import utcnow

DefaultNumeric = Annotated[Decimal, 20]


@as_declarative()
class Base:
    registry = registry(
        type_annotation_map={
            DefaultNumeric: Numeric(20, 4),  # noqa: WPS432
        },
    )

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=utcnow(),
        onupdate=utcnow(),
    )
