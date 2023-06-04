import csv
import mimetypes
from io import StringIO
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Header, HTTPException, UploadFile, status

from banki import vo
from banki.api.v1 import deps, schemas
from banki.use_cases.debts import CreateDebtsInput, CreateDebtsUseCase, PayDebtInput, PayDebtUseCase
from banki.use_cases.errors import Details

router = APIRouter()


@router.post(
    '',
    name='Batch debts import',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {'model': Details},
    },
)
def create(
    body: str = Body(),
    content_type: Annotated[str | None, Header()] = None,
    create_debts: CreateDebtsUseCase = Depends(deps.create_debts),
) -> schemas.ImportDebtsRep:
    if content_type != mimetypes.types_map['.csv']:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Expecting 'text/csv' media type, '{content_type}' was given",
        )

    parsed_csv = csv.DictReader(StringIO(body), delimiter=',')
    debt_list = []
    for debt in parsed_csv:
        debt_list.append(
            vo.ImportDebtInfo(
                name=debt.get('name', None),
                government_id=debt.get('governmentId', None),
                email=debt.get('email', None),  # type: ignore[arg-type]
                debt_id=debt.get('debtId', None),  # type: ignore[arg-type]
                debt_amount=debt.get('debtAmount', None),  # type: ignore[arg-type]
                debt_due_date=debt.get('debtDueDate', None),  # type: ignore[arg-type]
            ),
        )

    output = create_debts(CreateDebtsInput(debts=debt_list))

    return schemas.ImportDebtsRep(
        created_persons_count=output.created_persons_count,
        created_debts_count=output.created_debts_count,
    )


@router.post(
    '/file',
    name='Batch debts import uploading a file',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {'model': Details},
    },
)
def create_with_file(
    file: UploadFile,  # noqa: WPS110
    create_debts: CreateDebtsUseCase = Depends(deps.create_debts),
) -> schemas.ImportDebtsRep:
    if file.content_type != mimetypes.types_map['.csv']:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Expecting 'text/csv' media type, '{file.content_type}' was given",
        )

    parsed_csv = csv.DictReader(
        StringIO(file.file.read().decode('utf-8')),
        delimiter=',',
    )

    debt_list = []
    for debt in parsed_csv:  # TODO: Use `get` instead of direct accessing
        debt_list.append(
            vo.ImportDebtInfo(
                name=debt.get('name', None),
                government_id=debt.get('governmentId', None),
                email=debt.get('email', None),  # type: ignore[arg-type]
                debt_id=debt.get('debtId', None),  # type: ignore[arg-type]
                debt_amount=debt.get('debtAmount', None),  # type: ignore[arg-type]
                debt_due_date=debt.get('debtDueDate', None),  # type: ignore[arg-type]
            ),
        )

    output = create_debts(CreateDebtsInput(debts=debt_list))

    return schemas.ImportDebtsRep(
        created_persons_count=output.created_persons_count,
        created_debts_count=output.created_debts_count,
    )


@router.patch(
    '/webhook',
    name='Webhook to receive debt updates',
)
def debt_webhook(
    body: schemas.PayDebtWebhookReq,
    pay_debt: PayDebtUseCase = Depends(deps.pay_debt),
) -> schemas.Debt:
    debt = pay_debt(
        PayDebtInput(
            debt_id=body.debt_id,
            paid_at=body.paid_at,
            paid_amount=body.paid_amount,
            paid_by=body.paid_by,
        ),
    ).debt

    return schemas.Debt.from_entity(debt)
