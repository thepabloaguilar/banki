from decimal import Decimal

from banki.use_cases.errors import Details, DomainError, Reason


class DebtDoesNotExist(DomainError):
    reason = Reason.NOT_FOUND

    def __init__(self, debt_id: int) -> None:
        details: Details = {
            'message': 'debt not found',
            'error_details': {
                'debt_id': debt_id,
            },
        }
        super().__init__(details)


class EmptyPersonName(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self) -> None:
        details: Details = {
            'message': 'invalid person name, it has no value',
            'error_details': {},
        }
        super().__init__(details)


class EmptyGovernmentID(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self) -> None:
        details: Details = {
            'message': 'invalid government id, it has no value',
            'error_details': {},
        }
        super().__init__(details)


class InvalidDebtID(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self, debt_id: int) -> None:
        details: Details = {
            'message': 'invalid debt id, it must be greater than zero',
            'error_details': {
                'debt_id': debt_id,
            },
        }
        super().__init__(details)


class InvalidDebtAmount(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self, amount: Decimal) -> None:
        details: Details = {
            'message': 'invalid debt amount, it must be greater than zero',
            'error_details': {
                'amount': str(amount),
            },
        }
        super().__init__(details)


class InvalidPaidAmount(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self, amount: Decimal) -> None:
        details: Details = {
            'message': 'invalid paid amount, it must be greater than zero',
            'error_details': {
                'amount': str(amount),
            },
        }
        super().__init__(details)


class EmptyPaidBy(DomainError):
    reason = Reason.INVALID_DATA

    def __init__(self) -> None:
        details: Details = {
            'message': 'invalid paid by, it has no value',
            'error_details': {},
        }
        super().__init__(details)
