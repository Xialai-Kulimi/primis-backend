from datetime import datetime

from fastapi import WebSocket
from pydantic import BaseModel

from backend.utils.mongo import global_db
from backend.utils.console import console


user_collection = global_db.user

class ClientInfo(BaseModel):
    token: str
    server = 'primis'
    login_time = datetime.now()

class User():
    def __init__(self, token: str) -> None:
        
        self.raw_data = user_collection.find_one({'token': token})
        if self.raw_data == None:
            self.valid = False
        else:
            self.valid = True

class Client():
    def __init__(self, websocket: WebSocket, client_info: ClientInfo):
        self.websocket = websocket
        self.info = client_info
        self.server = client_info.server
        self.user = User(token=client_info.token)
        
    