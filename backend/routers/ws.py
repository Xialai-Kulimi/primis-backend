import asyncio
from typing import List
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from backend.utils.console import console
from backend.controller import controller

from backend.dependencies import get_cookie_or_token
from backend.auth import User, ClientInfo, Client

manager = controller.manager.manager
handler = controller.handler.handler


router = APIRouter(
    prefix="/api/ws",
    tags=["ws"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, cookie_or_token: str = Depends(get_cookie_or_token)):
    """websocket entry endpoint

    1. validate the token
    2. create client instance
    3. append to manager

    4. send receive data to handler (loop)

    Args:
        websocket (WebSocket): websocket (wss://)
        cookie_or_token (str, optional): should be token

    Raises:
        HTTPException: when the token is invalid
    """


    client_info = ClientInfo(token=cookie_or_token)
    client = Client(websocket, client_info)
    if not client.user.valid:
        raise HTTPException(status_code=403, detail="invalid token")
    await manager.connect(client)
    try:
        while True:
            data = await websocket.receive_json()
            await handler(client, data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
