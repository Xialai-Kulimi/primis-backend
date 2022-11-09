
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import asyncio
from backend.utils.console import console
from datetime import datetime
from backend.controller import controller

manager = controller.manager.manager


router = APIRouter(
    prefix="/api/ws",
    tags=["ws"],
    responses={404: {"description": "Not found"}},
)








@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:

            data = await websocket.receive_json()
            console.log(data)
            if data.get('content'):
                await websocket.send_json({'type': 'caption', 'message': [{'class': '', 'message': f'你說：「{data["content"]}」'}, ]})
            await websocket.send_json({'type': 'caption', 'message': [{'class': 'primary--text', 'message': 'primary color test'}, ]})
            await websocket.send_json({'type': 'surrounding', 'message': [{'class': 'primary--text', 'message': 'primary color test'}, ]})
            await websocket.send_json({'type': 'status', 'message': [{'class': 'primary--text', 'message': 'primary color test'}, ]})
            await websocket.send_json({
                'type': 'target',
                'buttons': [
                    {
                        'text': 'text1',
                        'id': 'btn1',
                        'color': 'primary',
                        'list': [
                            {'text': 'text', 'value': 'value'},
                            {'text': 'text2', 'value': 'value2'},
                            {'text': 'text3', 'value': 'value3'},
                        ]
                    },
                    {
                        'text': 'text2',
                        'id': 'btn2',
                        'color': 'error',
                        'list': [
                            {'text': 'text', 'value': 'value'},
                            {'text': 'text2', 'value': 'value2'},
                            {'text': 'text3', 'value': 'value3'},
                        ]
                    },
                ]
            })
            await websocket.send_json({
                'type': 'reachable',
                'buttons': [
                    {
                        'text': 'text1',
                        'id': 'btn3231',
                        'color': 'primary',
                        'list': [
                            {'text': 'text', 'value': 'value'},
                            {'text': 'text2', 'value': 'value2'},
                            {'text': 'text3', 'value': 'value3'},
                        ]
                    },
                    {
                        'text': 'text2',
                        'id': 'btn22323',
                        'color': 'info',
                        'list': [
                            {'text': 'text', 'value': 'value78'},
                            {'text': 'text2', 'value': 'value27878'},
                            {'text': 'text3', 'value': 'value37878'},
                        ]
                    },
                ]
            })
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")