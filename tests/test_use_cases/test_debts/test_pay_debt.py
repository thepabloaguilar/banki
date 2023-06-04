from datetime import date, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from returns.functions import identity

from banki import entities
from banki.use_cases.debts import errors
from banki.use_cases.debts.pay_debt import DbGateway, PayDebtInput, PayDebtOutput, PayDebtUseCase


@pytest.fixture()
def db() -> Mock:
    return Mock(spec=DbGateway)


def test_should_update_unpaid_debt_to_paid(db: Mock) -> None:
    debt = entities.Debt(
        id=1,
        person_id=1,
        amount=Decimal(100),
        due_date=date.today(),
        status=entities.DebtStatus.NON_PAID,
        paid_at=None,
        paid_amount=None,
        paid_by=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    uc = PayDebtUseCase(db=db)
    inp = PayDebtInput(
        debt_id=debt.id,
        paid_at=datetime.now(),
        paid_amount=Decimal(100),
        paid_by='Matue',
    )
    expected_output = PayDebtOutput(
        debt=entities.Debt(
            id=debt.id,
            person_id=debt.person_id,
            amount=debt.amount,
            due_date=debt.due_date,
            status=entities.DebtStatus.PAID,
            paid_at=inp.paid_at,
            paid_amount=inp.paid_amount,
            paid_by=inp.paid_by,
            created_at=debt.created_at,
            updated_at=debt.updated_at,
        ),
    )

    db.get_debt_by_id.return_value = debt
    db.update_debt.side_effect = identity

    output = uc(inp)

    db.get_debt_by_id.assert_called_once_with(debt.id)
    db.update_debt.assert_called_once_with(expected_output.debt)
    assert output == expected_output


def test_should_do_nothing_when_debt_is_already_paid(db: Mock) -> None:
    debt = entities.Debt(
        id=1,
        person_id=1,
        amount=Decimal(100),
        due_date=date.today(),
        status=entities.DebtStatus.PAID,
        paid_at=datetime.now(),
        paid_amount=Decimal(100),
        paid_by='MHRAP',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    uc = PayDebtUseCase(db=db)
    inp = PayDebtInput(
        debt_id=debt.id,
        paid_at=datetime.now(),
        paid_amount=Decimal(100),
        paid_by='Matue',
    )
    expected_output = PayDebtOutput(debt=debt)

    db.get_debt_by_id.return_value = debt

    output = uc(inp)

    db.get_debt_by_id.assert_called_once_with(debt.id)
    db.update_debt.assert_not_called()
    assert output == expected_output


def test_should_raise_an_exception_when_debt_id_is_lower_or_equal_to_zero(db: Mock) -> None:
    uc = PayDebtUseCase(db=db)
    inp = PayDebtInput(
        debt_id=0,
        paid_at=datetime.now(),
        paid_amount=Decimal(100),
        paid_by='Matue',
    )

    with pytest.raises(errors.InvalidDebtID):
        uc(inp)


def test_should_raise_an_exception_when_paid_amount_is_lower_or_equal_to_zero(db: Mock) -> None:
    uc = PayDebtUseCase(db=db)
    inp = PayDebtInput(
        debt_id=1,
        paid_at=datetime.now(),
        paid_amount=Decimal(0),
        paid_by='Matue',
    )

    with pytest.raises(errors.InvalidPaidAmount):
        uc(inp)


def test_should_raise_an_exception_when_paid_by_is_empty(db: Mock) -> None:
    uc = PayDebtUseCase(db=db)
    inp = PayDebtInput(
        debt_id=1,
        paid_at=datetime.now(),
        paid_amount=Decimal(1),
        paid_by=' ',
    )

    with pytest.raises(errors.EmptyPaidBy):
        uc(inp)
