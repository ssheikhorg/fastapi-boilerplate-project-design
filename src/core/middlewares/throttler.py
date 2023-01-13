"""throttler for api rate limit"""

from starlette.types import Receive, Scope, Send, ASGIApp

from ..cache.base import BaseBackend


class ThrottleMiddleware:
    """Throttle middleware."""

    def __init__(self, app: ASGIApp, backend: BaseBackend):
        self.app = app
        self.backend = backend

        assert self.backend is not None, "Backend is not configured"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Call method."""
        if scope["type"] not in ("http", "https"):
            return await self.app(scope, receive, send)

        # return response if method is GET with no rate limit
        if scope["method"] == "GET":
            return await self.app(scope, receive, send)

        # global rate limit key to get request rate
        rate_limit_key = "rate_per_minute"
        # get client ip address
        client_ip = scope["client"][0]

        # dynamic rate limit to be set for each endpoint
        match scope["path"]:
            case "/test":
                # override global rate limit
                rate_limit_key = "rate_limit"
                rate_limit = await self._rate_limit_global_method(client_ip, rate_limit_key)

                if rate_limit["success"]:
                    return await self.app(scope, receive, send)
                else:
                    return await block_request()(scope, receive, send)

            case _:
                rate_limit = await self._rate_limit_global_method(client_ip, rate_limit_key)

                if rate_limit["success"]:
                    return await self.app(scope, receive, send)
                else:
                    return await block_request()(scope, receive, send)

    async def _rate_limit_global_method(self, client_ip: str, rl_key: str):
        """Rate limit global method."""
        default_rate_limit = "20"
        default_expiry = 60

        # get rate limit from redis
        request_rate = await self.backend.get(rl_key)
        if request_rate is None:
            await self.backend.set(rl_key, default_rate_limit)

        # get client rate
        client_rate = await self.backend.get(client_ip)

        if client_rate:
            # check if client rate is greater than request rate
            if int(client_rate) >= int(request_rate):
                return {"success": False}
            else:
                # increment client rate
                await self.backend.incr(client_ip)
        else:
            # set client rate
            await self.backend.set(client_ip, "1", default_expiry)

        return {"success": True}


def block_request() -> ASGIApp:
    """Block request."""

    async def request_limit_error(scope: Scope, receive: Receive, send: Send) -> None:
        await send({"type": "http.response.start", "status": 429, "headers": [[b"content-type", b"application/json"]]})
        await send({
            "type": "http.response.body",
            "body": b'{"msg": "Too many requests, please try later.", "statusCode": 429}'
        })

    return request_limit_error
