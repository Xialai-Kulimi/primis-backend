from os import getenv

from fastapi import Depends, FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.dependencies import login
from backend.routers import entity, ws
from backend.controller import controller

app = FastAPI(dependencies=[Depends(login)])
app.add_middleware(SessionMiddleware, secret_key=getenv("OAUTH2_CLIENT_SECRET"))
app.include_router(entity.router)
app.include_router(ws.router)


import asyncio
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(controller.main.main())
    