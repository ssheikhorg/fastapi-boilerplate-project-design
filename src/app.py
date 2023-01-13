from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware

from src import settings as c
from src.core.error import http_error, validation_error
from src import RedisBackend
from src.core.middlewares.throttler import ThrottleMiddleware
from src.core.utils.base_response import UnicornException
from src.core.utils.events import create_start_app_handler, create_stop_app_handler


def init_routers(app_: FastAPI) -> None:
    app_.include_router(tests1.router, tags=["tests1"])
    app_.include_router(tests2.router)


def init_exception_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(HTTPException, http_error.http_error_handler)
    app_.add_exception_handler(UnicornException, http_error.unicorn_exception_handler)
    app_.add_exception_handler(RequestValidationError, validation_error.http422_error_handler)
    app_.add_exception_handler(RequestValidationError, validation_error.request_validation_exception_handler)
    app_.add_exception_handler(TypeError, validation_error.type_error_exception_handler)


def init_middleware() -> list:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            ThrottleMiddleware,
            backend=RedisBackend(),
        ),
    ]


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Python APIs",
        description="Python server apis",
        version="0.1.0",
        docs_url=None if not c.debug_mode else "/",  # disable swagger docs in production
        openapi_url=None if not c.debug_mode else "/v1/openapi.json",  # disable swagger docs in production
        redoc_url=None,
        middleware=init_middleware(),
    )

    """fastapi event handlers"""
    app_.add_event_handler("startup", create_start_app_handler(app_))
    app_.add_event_handler("shutdown", create_stop_app_handler(app_))

    """add routers"""
    init_routers(app_)

    """add exception handlers"""
    init_exception_handlers(app_)

    return app_


app = create_app()


# @app.post("/test")
# async def test(body: dict, backend: RedisBackend = Depends(RedisBackend)) -> dict:
#     await backend.set("rate_per_minute", "5")
#     return {"message": "test"}
