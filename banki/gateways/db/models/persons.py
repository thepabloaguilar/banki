from sqlalchemy.orm import Mapped, mapped_column, relationship

from banki import entities
from banki.gateways.db.models import Base, Debt


class Person(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    government_id: Mapped[str]
    email: Mapped[str]

    debts: Mapped[list['Debt']] = relationship()

    def to_entity(self) -> entities.Person:
        return entities.Person(
            id=self.id,
            name=self.name,
            government_id=self.government_id,
            email=self.email,  # type: ignore[arg-type]
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
