from typing import Any

import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src import settings as c
from src.core.utils.base_response import HttpResponse as Rs


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        self.secret = c.jwt_secret
        self.algorithm = c.jwt_algorithm
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        try:
            decoded_token = self.decode_jwt(token)
            if decoded_token:
                is_token_valid = True
                return is_token_valid
        except Exception as e:
            raise e

    def decode_jwt(self, token: str) -> Any | None:
        try:
            decoded_token = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return decoded_token
        except jwt.exceptions.InvalidSignatureError:
            return None
        except Exception as e:
            return Rs.server_error(e.__str__())
