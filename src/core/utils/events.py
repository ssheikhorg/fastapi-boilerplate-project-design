"""FastAPI events"""
from typing import Callable
from fastapi import FastAPI

from src import MongoEvent


def create_start_app_handler(_: FastAPI) -> Callable:
    """FastAPI event handler for startup"""

    async def start_app() -> None:
        await MongoEvent().start()

    return start_app


def create_stop_app_handler(_: FastAPI) -> Callable:
    """FastAPI event handler for shutdown"""

    async def stop_app() -> None:
        """FastAPI event handler for shutdown"""
        await MongoEvent().stop()

    return stop_app
