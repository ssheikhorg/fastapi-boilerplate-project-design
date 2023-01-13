from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status as s


class HttpResponse(JSONResponse):
    def __init__(self, data=None, msg=None, status_code=s.HTTP_200_OK):
        super().__init__(
            {
                "statusCode": status_code,
                "data": jsonable_encoder(data) or [],
                "msg": msg or "Success",
            },
            status_code=s.HTTP_200_OK if status_code == s.HTTP_201_CREATED else status_code,
            headers={"Content-Type": "application/json"},
        )

    @classmethod
    def success(cls, data=None, msg=None):
        return cls(data=data, msg=msg)

    @classmethod
    def not_found(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Not found", status_code=s.HTTP_404_NOT_FOUND)

    @classmethod
    def conflict(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Conflict", status_code=s.HTTP_409_CONFLICT)

    @classmethod
    def created(cls, data=None, msg=None):
        return cls(data=data, msg=msg, status_code=s.HTTP_201_CREATED)

    @classmethod
    def not_created(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Not created", status_code=s.HTTP_400_BAD_REQUEST)

    @classmethod
    def modified(cls, data=None, msg=None):
        return cls(data=data, msg=msg)

    @classmethod
    def deleted(cls, data=None, msg=None):
        return cls(data=data, msg=msg)

    @classmethod
    def bad_request(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Bad request", status_code=s.HTTP_400_BAD_REQUEST)

    @classmethod
    def unauthorized(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Unauthorized", status_code=s.HTTP_401_UNAUTHORIZED)

    @classmethod
    def server_error(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Server error", status_code=s.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def not_acceptable(cls, data=None, msg=None):
        return cls(data=data, msg=msg or "Not acceptable", status_code=s.HTTP_406_NOT_ACCEPTABLE)


class UnicornException(Exception):
    def __init__(self, code, errmsg, data=None):
        self.code = code
        self.errmsg = errmsg
        self.data = data or {}
