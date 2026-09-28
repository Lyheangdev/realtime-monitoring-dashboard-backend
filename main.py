from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from json import dumps as json_dumps, loads as Json_parse
from typing import List
from enum import Enum
from pydantic import BaseModel

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


class Station(str, Enum):
    LNK = "lnk"
    SMT = "smt"
    IMT = "imt"

# Type
class IStation(BaseModel):
    name : str 
    description : str | None = None


app  = FastAPI()
socketManager = SocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await socketManager.connect(socket=websocket)
        while True:
            data = await websocket.receive_text()
            await socketManager.broadcast(data)

    except WebSocketDisconnect:
        print("Client disconnected")
       
@app.get("/api/station/{station_name}")
async def getStation(station_name: Station):
    if station_name is Station.IMT:
        return {"data": f"Hey: {station_name.value}"}
    else:
        return {"data": station_name}

@app.post("/api/station")
async def register_station(station: IStation):
    return {"data": {**station.model_dump()}}

@app.get("/")
async def root():
    return {"message" : "Hello World!"}