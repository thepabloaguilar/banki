from typing import assert_never

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from banki.api.v1 import api_router
from banki.configuration import settings
from banki.use_cases.errors import Details, DomainError, Reason

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    ),
]

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    middleware=middleware,
    contact={
        'name': 'Pablo Aguilar',
        'url': 'https://thepabloaguilar.dev/',
        'email': 'pablo.aguilar@outlook.com.br',
    },
)

app.include_router(api_router, prefix='/api/v1')


@app.exception_handler(DomainError)
def domain_exceptions_handler(req: Request, exc: DomainError) -> JSONResponse:
    match exc.reason:
        case Reason.INVALID_DATA:
            status_code = status.HTTP_400_BAD_REQUEST
        case Reason.PRECONDITION_FAILED:
            status_code = status.HTTP_412_PRECONDITION_FAILED
        case Reason.NOT_FOUND:
            status_code = status.HTTP_404_NOT_FOUND
        case Reason.FORBIDDEN:
            status_code = status.HTTP_403_FORBIDDEN
        case Reason.UNKNOWN:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        case _ as unreachable:
            assert_never(unreachable)

    return JSONResponse(content=exc.details, status_code=status_code)


@app.exception_handler(HTTPException)
def http_exception_handler(req: Request, exc: HTTPException) -> JSONResponse:
    details: Details = {
        'message': exc.detail,
        'error_details': {},
    }

    return JSONResponse(content=details, status_code=exc.status_code)
