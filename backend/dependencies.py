
from fastapi import Cookie, WebSocket, status

from backend.utils.console import console


async def get_token(
    websocket: WebSocket = None,
    token: str | None = Cookie(default=None),
):
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return token
