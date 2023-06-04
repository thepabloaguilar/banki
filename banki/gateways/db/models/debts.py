from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from banki import entities
from banki.gateways.db.models import Base, DefaultNumeric

if TYPE_CHECKING:
    from banki.gateways.db.models import Person


class Debt(Base):
    __tablename__ = 'debts'

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id'))
    amount: Mapped[DefaultNumeric]
    due_date: Mapped[date]
    status: Mapped[entities.DebtStatus]
    paid_at: Mapped[datetime] = mapped_column(nullable=True)
    paid_amount: Mapped[DefaultNumeric] = mapped_column(nullable=True)
    paid_by: Mapped[str] = mapped_column(nullable=True)

    person: Mapped['Person'] = relationship(back_populates='debts')

    def to_entity(self) -> entities.Debt:
        return entities.Debt(
            id=self.id,
            person_id=self.person_id,
            amount=self.amount,
            due_date=self.due_date,
            status=self.status,
            paid_at=self.paid_at,
            paid_amount=self.paid_amount,
            paid_by=self.paid_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
