from sqlalchemy import text

from banki.gateways.db.repos.base_repo import BaseRepo


class Health(BaseRepo):
    def is_health(self) -> bool:
        try:
            with self._get_session() as session:
                session.execute(text('SELECT 1'))
        except Exception:
            return False
        return True
