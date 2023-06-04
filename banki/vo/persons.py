from pydantic import EmailStr
from pydantic.dataclasses import dataclass


@dataclass
class Person:
    name: str
    government_id: str
    email: EmailStr

    def __hash__(self) -> int:
        return hash(self.government_id)
