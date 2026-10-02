from fastapi import WebSocket
from typing import List

"""
@Description: Websocket manager configuration
@Purpose: Support multi sturbs
"""
class SocketManager:
    def __init__(self):
        self.sockets: List[WebSocket] = []

    async def connect(self, socket: WebSocket):
        await socket.accept()
        self.sockets.append(socket)

    def disconnect(self, websocket: WebSocket):
        self.sockets.remove(websocket)

    async def push_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connected_sturb in self.sockets:
            await connected_sturb.send_text(message)