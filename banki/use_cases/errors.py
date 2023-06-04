from enum import StrEnum, auto
from typing import Any, Optional, TypedDict


class Reason(StrEnum):
    UNKNOWN = auto()
    INVALID_DATA = auto()
    PRECONDITION_FAILED = auto()
    NOT_FOUND = auto()
    FORBIDDEN = auto()


class Details(TypedDict):
    message: str
    error_details: Optional[dict[str, Any]]


class DomainError(Exception):
    reason: Reason = Reason.UNKNOWN

    details: Details

    def __init__(self, details: Details) -> None:
        self.details = details
        super().__init__(details['message'])
