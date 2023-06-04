from banki.api.v1 import schemas


class HealthCheckRep(schemas.BaseAPIModel):
    health: bool
