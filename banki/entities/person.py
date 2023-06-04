from datetime import datetime

from pydantic import BaseModel, EmailStr


class Person(BaseModel):
    id: int
    name: str
    government_id: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
