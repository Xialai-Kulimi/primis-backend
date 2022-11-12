import asyncio
from typing import List
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends

from backend.dependencies import get_token
from backend.auth import User, ClientInfo, Client

from backend.controller import controller
console = controller.utils.console
manager = controller.manager.manager
handler = controller.handler.handler


router = APIRouter(
    tags=["ws"],
    responses={404: {"description": "Not found"}},
)

# @router.get("/api/ws")
# async def api_ws_test(cookie_or_token: str = Depends(get_token())):
#     console.log(cookie_or_token)
#     return HTTPException(status_code=404)

@router.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    """websocket entry endpoint

    1. validate the token
    2. create client instance
    3. append to manager

    4. send receive data to handler (loop)

    Args:
        websocket (WebSocket): websocket (wss://)
        token (str): should be token

    Raises:
        HTTPException: when the token is invalid
    """

    client_info = ClientInfo(token=token)
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
