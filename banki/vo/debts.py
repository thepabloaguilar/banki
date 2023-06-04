from datetime import date, datetime
from decimal import Decimal

from pydantic import EmailStr
from pydantic.dataclasses import dataclass

from banki import entities


@dataclass
class Debt:
    debt_id: int
    person_id: int
    amount: Decimal
    status: entities.DebtStatus
    due_date: date


@dataclass
class ImportDebtInfo:
    name: str
    government_id: str
    email: EmailStr
    debt_id: int
    debt_amount: Decimal
    debt_due_date: date


@dataclass
class PayDebt:
    debt_id: int
    paid_at: datetime
    paid_amount: Decimal
    paid_by: str
