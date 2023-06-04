from fastapi import BackgroundTasks, Depends

from banki.gateways.db.repos.debts import Debts as DbDebts
from banki.gateways.db.repos.health import Health as DbHealth
from banki.gateways.email.client import EmailClient
from banki.use_cases.debts import CreateDebtsUseCase, PayDebtUseCase
from banki.use_cases.health import HealthCheckUseCase


def health_check(db: DbHealth = Depends()) -> HealthCheckUseCase:
    return HealthCheckUseCase(db=db)


def create_debts(background_tasks: BackgroundTasks, db: DbDebts = Depends()) -> CreateDebtsUseCase:
    return CreateDebtsUseCase(
        db=db,
        email=EmailClient(background_tasks),
    )


def pay_debt(db: DbDebts = Depends()) -> PayDebtUseCase:
    return PayDebtUseCase(db=db)
