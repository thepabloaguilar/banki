from typing import Optional

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from banki import entities, vo
from banki.gateways.db.models import Debt, Person
from banki.gateways.db.repos.base_repo import BaseRepo


class Debts(BaseRepo):
    def get_person_by_government_id(self, government_id: str) -> Optional[entities.Person]:
        with self._get_session() as session:
            db_person = (
                session.query(Person)
                .filter(Person.government_id == government_id)
                .first()
            )
            if db_person:
                return db_person.to_entity()
        return None

    def create_person(self, person: vo.Person) -> entities.Person:
        with self._get_session() as session:
            db_person = Person(
                name=person.name,
                government_id=person.government_id,
                email=person.email,
            )

            session.add(db_person)
            session.commit()
            session.refresh(db_person)

            return db_person.to_entity()

    def create_debts_if_not_exist(self, debts: list[vo.Debt]) -> list[entities.Debt]:
        with self._get_session() as session:
            values_to_insert = [
                {
                    'id': debt.debt_id,
                    'person_id': debt.person_id,
                    'amount': debt.amount,
                    'due_date': debt.due_date,
                    'status': debt.status,
                }
                for debt in debts
            ]

            insert_stmt = (
                insert(Debt)
                .values(values_to_insert)
                .on_conflict_do_nothing(index_elements=['id'])
                .returning(Debt)
            )

            inserted_debts = session.execute(insert_stmt).fetchall()
            session.commit()

            if inserted_debts:
                inserted_debts = inserted_debts[0]

            return [
                inserted_debt.to_entity() for inserted_debt in inserted_debts
            ]

    def get_debt_by_id(self, debt_id: int) -> Optional[entities.Debt]:
        with self._get_session() as session:
            db_debt = (
                session.query(Debt)
                .filter(Debt.id == debt_id)
                .first()
            )
            if db_debt:
                return db_debt.to_entity()
        return None

    def update_debt(self, debt: entities.Debt) -> entities.Debt:
        with self._get_session() as session:
            stmt = (
                update(Debt)
                .filter(Debt.id == debt.id)
                .values(
                    person_id=debt.person_id,
                    amount=debt.amount,
                    due_date=debt.due_date,
                    status=debt.status,
                    paid_at=debt.paid_at,
                    paid_amount=debt.paid_amount,
                    paid_by=debt.paid_by,
                ).returning(Debt)
            )

            updated_debt = session.execute(stmt).first()[0]
            session.commit()

            return updated_debt.to_entity()
