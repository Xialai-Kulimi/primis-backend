import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import RedirectResponse
from pydantic.error_wrappers import ValidationError

from backend.dependencies import get_token
from backend.auth import ClientInfo, Client

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

    if client.user.raw_data.get('create_time', 0) > 1668932432 and not client.user.raw_data.get('allow_beta'):
        await client.websocket.accept()
        try:
            while True:
                await client.websocket.send_json({'type': 'operation', 'list': {
                        'title': "很抱歉",
                        'subtitle': "現在正在封測中",
                        'persistent': True,
                        'id': "",
                        'list': [],
                    }})
                await asyncio.sleep(696969)
        except WebSocketDisconnect:
            pass

    console.log('login: ', client.user.raw_data.get('username', 'no_username'))
    await manager.connect(client)
    async def read_from_socket(websocket: WebSocket):
        # nonlocal json_data
        try:
            async for data in websocket.iter_json():
            # json_data = data
                try:
                    asyncio.gather(handler(client, data))
                except Exception:
                    console.print_exception(show_locals=True)
        except WebSocketDisconnect:
            console.log('disconnect: ', client.user.raw_data.get('username', 'no_username'))
            await manager.disconnect(client)
        console.log('disconnect: ', client.user.raw_data.get('username', 'no_username'))
        await manager.disconnect(client)

    handle_loop = asyncio.create_task(read_from_socket(websocket))

    await asyncio.gather(handle_loop)
