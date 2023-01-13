#! /usr/bin/env python3.10

import uvicorn
from src import settings as c
# import typer


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="127.0.0.1",
                port=c.port, reload=c.debug_mode)
    # # typer.run(app, host=core.HOST, port=core.PORT)
    # typer.run(main)
