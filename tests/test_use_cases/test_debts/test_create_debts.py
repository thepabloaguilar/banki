from datetime import date, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from banki import entities, vo
from banki.use_cases.debts import errors
from banki.use_cases.debts.create_debts import (
    CreateDebtsInput,
    CreateDebtsOutput,
    CreateDebtsUseCase,
    DbGateway,
    EmailGateway,
)


@pytest.fixture()
def db() -> Mock:
    return Mock(spec=DbGateway)


@pytest.fixture()
def email() -> Mock:
    return Mock(spec=EmailGateway)


def test_should_create_a_person_if_not_exist_using_government_id(db: Mock, email: Mock) -> None:
    person = entities.Person(
        id=1,
        name='MC Igu',
        government_id='000000000',
        email='igu@test.com',  # type: ignore[arg-type]
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    vo_debt = vo.Debt(
        debt_id=1,
        person_id=person.id,
        status=entities.DebtStatus.NON_PAID,
        amount=Decimal(99),
        due_date=date.today(),
    )
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name=person.name,
                government_id=person.government_id,
                email=person.email,
                debt_id=vo_debt.debt_id,
                debt_amount=vo_debt.amount,
                debt_due_date=vo_debt.due_date,
            ),
        ],
    )
    expected_output = CreateDebtsOutput(
        created_persons_count=1,
        created_debts_count=1,
    )

    db.get_person_by_government_id.return_value = None
    db.create_person.return_value = person
    db.create_debts_if_not_exist.return_value = [
        entities.Debt(
            id=vo_debt.debt_id,
            person_id=vo_debt.person_id,
            amount=vo_debt.amount,
            due_date=vo_debt.due_date,
            status=vo_debt.status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

    output = uc(inp)

    db.create_person.assert_called_once()
    db.create_debts_if_not_exist.assert_called_once_with([vo_debt])
    email.send_charge_email.assert_called_once()
    assert output == expected_output


def test_should_not_create_a_person_with_the_government_id_exists(db: Mock, email: Mock) -> None:
    person = entities.Person(
        id=1,
        name='MC Igu',
        government_id='000000000',
        email='igu@test.com',  # type: ignore[arg-type]
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    vo_debt = vo.Debt(
        debt_id=1,
        person_id=person.id,
        status=entities.DebtStatus.NON_PAID,
        amount=Decimal(99),
        due_date=date.today(),
    )
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name=person.name,
                government_id=person.government_id,
                email=person.email,
                debt_id=vo_debt.debt_id,
                debt_amount=vo_debt.amount,
                debt_due_date=vo_debt.due_date,
            ),
        ],
    )
    expected_output = CreateDebtsOutput(
        created_persons_count=0,
        created_debts_count=1,
    )

    db.get_person_by_government_id.return_value = person
    db.create_debts_if_not_exist.return_value = [
        entities.Debt(
            id=vo_debt.debt_id,
            person_id=vo_debt.person_id,
            amount=vo_debt.amount,
            due_date=vo_debt.due_date,
            status=vo_debt.status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]

    output = uc(inp)

    db.create_person.assert_not_called()
    db.create_debts_if_not_exist.assert_called_once_with([vo_debt])
    assert output == expected_output


def test_should_raise_an_exception_when_name_is_empty(db: Mock, email: Mock) -> None:
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name='',
                government_id='0000000000',
                email='test@test.com',  # type: ignore[arg-type]
                debt_id=1,
                debt_amount=Decimal(1),
                debt_due_date=date.today(),
            ),
        ],
    )

    with pytest.raises(errors.EmptyPersonName):
        uc(inp)


def test_should_raise_an_exception_when_government_id_is_empty(db: Mock, email: Mock) -> None:
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name='Yunk Vino',
                government_id='',
                email='test@test.com',  # type: ignore[arg-type]
                debt_id=1,
                debt_amount=Decimal(1),
                debt_due_date=date.today(),
            ),
        ],
    )

    with pytest.raises(errors.EmptyGovernmentID):
        uc(inp)


def test_should_raise_an_exception_when_debt_id_is_lower_or_equal_to_zero(
    db: Mock,
    email: Mock,
) -> None:
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name='Yunk Vino',
                government_id='9999999999',
                email='test@test.com',  # type: ignore[arg-type]
                debt_id=0,
                debt_amount=Decimal(1),
                debt_due_date=date.today(),
            ),
        ],
    )

    with pytest.raises(errors.InvalidDebtID):
        uc(inp)


def test_should_raise_an_exception_when_debt_amount_is_lower_or_equal_to_zero(
    db: Mock,
    email: Mock,
) -> None:
    uc = CreateDebtsUseCase(db=db, email=email)
    inp = CreateDebtsInput(
        debts=[
            vo.ImportDebtInfo(
                name='Yunk Vino',
                government_id='9999999999',
                email='test@test.com',  # type: ignore[arg-type]
                debt_id=1,
                debt_amount=Decimal(0),
                debt_due_date=date.today(),
            ),
        ],
    )

    with pytest.raises(errors.InvalidDebtAmount):
        uc(inp)
