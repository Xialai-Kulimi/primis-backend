from fastapi import Depends, FastAPI

from backend.dependencies import get_token_header
from backend.routers import entity, ws, auth

app = FastAPI(dependencies=[Depends(get_token_header)])


app.include_router(entity.router)
app.include_router(ws.router)
app.include_router(auth.router)
