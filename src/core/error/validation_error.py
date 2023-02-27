from typing import Union, TypeVar, Callable
from pydantic import ValidationError
from fastapi import Request, status as s
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

T = TypeVar("T")
CBack = Callable[..., T]


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse(
        {
            "statusCode": s.HTTP_422_UNPROCESSABLE_ENTITY,
            "msg": "Unprocessable Entity",
            "data": exc.errors(),
        },
        status_code=s.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> CBack:
    return JSONResponse(
        {"statusCode": s.HTTP_400_BAD_REQUEST, "msg": "Bad Request", "data": exc.errors()},
        status_code=s.HTTP_400_BAD_REQUEST,
    )


async def type_error_exception_handler(_: Request, exc: TypeError) -> JSONResponse:
    return JSONResponse(
        {
            "statusCode": s.HTTP_422_UNPROCESSABLE_ENTITY,
            "msg": "Type Error",
            "data": str(exc),
        },
        status_code=s.HTTP_422_UNPROCESSABLE_ENTITY,
    )
