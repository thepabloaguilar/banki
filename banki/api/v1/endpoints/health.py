from fastapi import APIRouter, Depends

from banki.api.v1 import deps, schemas
from banki.use_cases.health import HealthCheckInput, HealthCheckUseCase

router = APIRouter()


@router.get('/check', response_model=schemas.HealthCheckRep, name='Health Check')
async def check(
    health_check: HealthCheckUseCase = Depends(deps.health_check),
) -> schemas.HealthCheckRep:
    out = health_check(HealthCheckInput())

    return schemas.HealthCheckRep(health=out.health)
