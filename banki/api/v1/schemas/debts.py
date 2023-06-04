from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from banki import entities
from banki.api.v1 import schemas


class Debt(schemas.BaseAPIModel):
    id: int
    person_id: int
    amount: Decimal
    due_date: date
    status: str  # TODO: Create ENUM for the API layer
    paid_at: Optional[datetime]
    paid_amount: Optional[Decimal]
    paid_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, debt: entities.Debt) -> 'Debt':
        return Debt(
            id=debt.id,
            person_id=debt.person_id,
            amount=debt.amount,
            due_date=debt.due_date,
            status=debt.status.name,
            paid_at=debt.paid_at,
            paid_amount=debt.paid_amount,
            paid_by=debt.paid_by,
            created_at=debt.created_at,
            updated_at=debt.updated_at,
        )


class ImportDebtsRep(schemas.BaseAPIModel):
    created_persons_count: int
    created_debts_count: int


class PayDebtWebhookReq(schemas.BaseAPIModel):
    debt_id: int
    paid_at: datetime
    paid_amount: Decimal
    paid_by: str
