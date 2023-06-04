from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel


class DebtStatus(StrEnum):
    PAID = auto()
    NON_PAID = auto()


class Debt(BaseModel):
    id: int
    person_id: int
    amount: Decimal
    due_date: date
    status: DebtStatus
    paid_at: Optional[datetime]
    paid_amount: Optional[Decimal]
    paid_by: Optional[str]
    created_at: datetime
    updated_at: datetime
