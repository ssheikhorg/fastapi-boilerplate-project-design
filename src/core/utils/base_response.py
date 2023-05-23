"""Helper functions for the bot."""
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Response
from starlette import status as s


class BaseResponse(JSONResponse):
    def __init__(self, data: Any = None, msg: str = None, status_code: int = s.HTTP_200_OK) -> None:
        super().__init__(
            {
                "statusCode": status_code,
                "data": jsonable_encoder(data) if data else [],
                "msg": msg if msg else "Success",
            },
            status_code=s.HTTP_200_OK if status_code in (s.HTTP_201_CREATED, s.HTTP_204_NO_CONTENT) else status_code,
            headers={"Content-Type": "application/json"},
        )

    @classmethod
    def success(cls, data: Any = None, msg: str = "Success") -> Response:
        return cls(data=data, msg=msg)

    @classmethod
    def not_found(cls, data: Any = None, msg: str = "Not found") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_204_NO_CONTENT)

    @classmethod
    def conflict(cls, data: Any = None, msg: str = "Conflict") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_409_CONFLICT)

    @classmethod
    def created(cls, data: Any = None, msg: str = "Created") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_201_CREATED)

    @classmethod
    def not_created(cls, data: Any = None, msg: str = "Not created") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_400_BAD_REQUEST)

    @classmethod
    def modified(cls, data: Any = None, msg: str = "Modified") -> Response:
        return cls(data=data, msg=msg)

    @classmethod
    def deleted(cls, data: Any = None, msg: str = "Deleted") -> Response:
        return cls(data=data, msg=msg)

    @classmethod
    def bad_request(cls, data: Any = None, msg: str = "Bad request") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_400_BAD_REQUEST)

    @classmethod
    def unauthorized(cls, data: Any = None, msg: str = "Unauthorized") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_401_UNAUTHORIZED)

    @classmethod
    def server_error(cls, data: Any = None, msg: str = "Something went wrong") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def not_acceptable(cls, data: Any = None, msg: str = "Not acceptable") -> Response:
        return cls(data=data, msg=msg, status_code=s.HTTP_406_NOT_ACCEPTABLE)


class UnicornExceptionError(Exception):
    def __init__(self, code: int, errmsg: str, data: Any = None) -> None:
        self.code = code
        self.errmsg = errmsg
        self.data = data or {}
