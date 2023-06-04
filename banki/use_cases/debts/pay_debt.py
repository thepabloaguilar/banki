from datetime import datetime
from decimal import Decimal
from typing import Optional, Protocol

from pydantic import BaseModel

from banki import entities
from banki.use_cases.debts import errors


class DbGateway(Protocol):
    def get_debt_by_id(self, debt_id: int) -> Optional[entities.Debt]:
        ...  # noqa: WPS428

    def update_debt(self, debt: entities.Debt) -> entities.Debt:
        ...  # noqa: WPS428


class PayDebtInput(BaseModel):
    debt_id: int
    paid_at: datetime
    paid_amount: Decimal
    paid_by: str


class PayDebtOutput(BaseModel):
    debt: entities.Debt


class PayDebtUseCase:
    _db: DbGateway

    def __init__(self, db: DbGateway) -> None:
        self._db = db

    def __call__(self, inp: PayDebtInput) -> PayDebtOutput:
        self._validate_input(inp)

        debt = self._db.get_debt_by_id(inp.debt_id)
        if not debt:
            raise errors.DebtDoesNotExist(inp.debt_id)

        if debt.status == entities.DebtStatus.NON_PAID:
            debt.paid_at = inp.paid_at
            debt.paid_amount = inp.paid_amount
            debt.paid_by = inp.paid_by.strip()
            debt.status = entities.DebtStatus.PAID

            debt = self._db.update_debt(debt)

        return PayDebtOutput(debt=debt)

    def _validate_input(self, inp: PayDebtInput) -> None:
        if inp.debt_id <= 0:
            raise errors.InvalidDebtID(inp.debt_id)

        if inp.paid_amount <= Decimal(0):
            raise errors.InvalidPaidAmount(inp.paid_amount)

        if not inp.paid_by.strip():
            raise errors.EmptyPaidBy()
