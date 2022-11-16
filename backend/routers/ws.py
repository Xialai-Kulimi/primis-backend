import asyncio
from typing import List
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic.error_wrappers import ValidationError

from backend.dependencies import get_token
from backend.auth import User, ClientInfo, Client

from backend.controller import controller
console = controller.utils.console.console
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
    try:
        client_info = ClientInfo(token=token)
        client = Client(websocket, client_info)
    except ValidationError:
        return RedirectResponse("/api/auth/me")
    if not client.user.valid:
        return RedirectResponse("/api/auth/login")

    console.log('login: ', client.user.raw_data.get('username', 'no_username'))
    await manager.connect(client)
    async def read_from_socket(websocket: WebSocket):
        # nonlocal json_data
        try:
            async for data in websocket.iter_json():
            # json_data = data
                await handler(client, data)
        except WebSocketDisconnect:
            console.log('disconnect: ', client.user.raw_data.get('username', 'no_username'))
            manager.disconnect(client)
        console.log('disconnect: ', client.user.raw_data.get('username', 'no_username'))
        manager.disconnect(client)

    handle_loop = asyncio.create_task(read_from_socket(websocket))
    
    await asyncio.gather(handle_loop)