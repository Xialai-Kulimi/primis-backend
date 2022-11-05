from os import getenv

from fastapi import Depends, FastAPI

from backend.dependencies import get_discord_id
from backend.routers import entity, ws
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(dependencies=[Depends(get_discord_id)])

app.add_middleware(SessionMiddleware, secret_key=getenv("OAUTH2_CLIENT_SECRET"))

app.include_router(entity.router)
app.include_router(ws.router)
