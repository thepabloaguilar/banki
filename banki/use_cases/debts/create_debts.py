from datetime import date
from decimal import Decimal
from typing import Optional, Protocol

from pydantic import BaseModel

from banki import entities, vo
from banki.use_cases.debts import errors


class DbGateway(Protocol):
    def get_person_by_government_id(self, government_id: str) -> Optional[entities.Person]:
        ...  # noqa: WPS428

    def create_person(self, person: vo.Person) -> entities.Person:
        ...  # noqa: WPS428

    def create_debts_if_not_exist(self, debts: list[vo.Debt]) -> list[entities.Debt]:
        ...  # noqa: WPS428


class EmailGateway(Protocol):
    def send_charge_email(self, email: str, name: str, amount: Decimal, due_date: date) -> None:
        ...  # noqa: WPS428


class CreateDebtsInput(BaseModel):
    debts: list[vo.ImportDebtInfo]


class CreateDebtsOutput(BaseModel):
    created_persons_count: int
    created_debts_count: int


class CreateDebtsUseCase:
    _db: DbGateway
    _email: EmailGateway

    def __init__(self, db: DbGateway, email: EmailGateway) -> None:
        self._db = db
        self._email = email

    def __call__(self, inp: CreateDebtsInput) -> CreateDebtsOutput:
        grouped_debts = self._group_debts_by_person(inp.debts)

        return self._process_debts(grouped_debts)

    def _group_debts_by_person(
        self,
        debts: list[vo.ImportDebtInfo],
    ) -> dict[vo.Person, list[vo.ImportDebtInfo]]:
        grouped_debts: dict[vo.Person, list[vo.ImportDebtInfo]] = {}
        for debt in debts:
            self._validate_debt(debt)

            person = vo.Person(
                name=debt.name.strip(),
                government_id=debt.government_id.strip(),
                email=debt.email,
            )

            if person not in grouped_debts:
                grouped_debts[person] = []

            grouped_debts[person].append(debt)

        return grouped_debts

    def _validate_debt(self, debt: vo.ImportDebtInfo) -> None:
        if not debt.name.strip():
            raise errors.EmptyPersonName()

        if not debt.government_id.strip():
            raise errors.EmptyGovernmentID()

        if debt.debt_id <= 0:
            raise errors.InvalidDebtID(debt.debt_id)

        if debt.debt_amount <= Decimal(0):
            raise errors.InvalidDebtAmount(debt.debt_amount)

    def _process_debts(
        self,
        grouped_debts: dict[vo.Person, list[vo.ImportDebtInfo]],
    ) -> CreateDebtsOutput:
        output = CreateDebtsOutput(
            created_persons_count=0,
            created_debts_count=0,
        )

        for vo_person, debts in grouped_debts.items():
            person = self._db.get_person_by_government_id(vo_person.government_id)
            if not person:
                person = self._db.create_person(vo_person)
                output.created_persons_count += 1

            output.created_debts_count += self._create_debts(person, debts)

        return output

    def _create_debts(self, person: entities.Person, debts: list[vo.ImportDebtInfo]) -> int:
        vo_debts = []
        for debt in debts:
            vo_debts.append(
                vo.Debt(
                    debt_id=debt.debt_id,
                    person_id=person.id,
                    status=entities.DebtStatus.NON_PAID,
                    amount=debt.debt_amount,
                    due_date=debt.debt_due_date,
                ),
            )

        new_debts = self._db.create_debts_if_not_exist(vo_debts)
        for new_debt in new_debts:
            self._email.send_charge_email(
                person.email,
                person.name,
                new_debt.amount,
                new_debt.due_date,
            )

        return len(new_debts)
