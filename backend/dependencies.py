from backend.utils.console import console
from typing import Union
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status, Request

async def login(session: Union[str, None]= Cookie(default=None)):
    # console.print(session)
    # console.log(session)
    return session

async def check_have_discord_id(request: Request):
    return request.session.get("session", None)

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token
