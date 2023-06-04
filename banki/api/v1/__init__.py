from fastapi import APIRouter

from banki.api.v1.endpoints import debts, health

api_router = APIRouter()

api_router.include_router(health.router, prefix='/health', tags=['health'])
api_router.include_router(debts.router, prefix='/debts', tags=['debts'])
