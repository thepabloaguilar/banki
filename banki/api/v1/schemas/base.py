from humps import camel
from pydantic import BaseModel


class BaseAPIModel(BaseModel):
    class Config:
        alias_generator = camel.case
        allow_population_by_field_name = True
