from os import getenv
import asyncio

from fastapi import Depends, FastAPI

from backend.routers import ws
from backend.controller import controller

app = FastAPI()
app.include_router(ws.router)


@app.on_event("startup")
async def startup_event():
    for t in controller.main.loop_list:
        asyncio.create_task(t())
