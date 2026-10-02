# Build-in/third-party modules
from contextlib import asynccontextmanager
from fastapi import WebSocket, WebSocketDisconnect

# Application modules
from config.core import app, socketManager

# Websocket entry-point
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await socketManager.connect(socket=websocket)
        while True:
            data = await websocket.receive_text()
            await socketManager.broadcast(data)

    except WebSocketDisconnect:
        socketManager.disconnect(websocket=websocket)
        print("Client disconnected")
