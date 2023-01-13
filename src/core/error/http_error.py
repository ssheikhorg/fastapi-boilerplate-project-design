from starlette.responses import JSONResponse
from fastapi import HTTPException, Request

from src.core.utils.base_response import UnicornException


async def http_error_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        {"statusCode": exc.status_code, "msg": "Something went wrong", "data": exc.detail}, status_code=exc.status_code
    )


async def unicorn_exception_handler(_: Request, exc: UnicornException) -> JSONResponse:
    return JSONResponse({"statusCode": exc.code, "msg": exc.errmsg, "data": exc.data})
