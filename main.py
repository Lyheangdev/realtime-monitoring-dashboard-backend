# Build-in/third-party modules
from fastapi import WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from datetime import datetime as dt


# Application modules
from .config.core import app, socketManager
from .config.redis import redisClientDepend
from .generators.sse_event_generator import seeEventGenerator

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


# testing with json-line
class LineJson(BaseModel):
    name: str
    description: str

live_lines_data = [
    LineJson(name="Plumbus", description="A multi-purpose household device."),
    LineJson(name="Portal Gun", description="A portal opening device."),
    LineJson(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@app.get("/api/v1/sse/stream")
async def streamSSE(request: Request, redis_client:redisClientDepend):
   
   print(f"-------------   | SSE CONNECTION STUB | ----------------")
   print()
   print(f"| Established at: {dt.now()}")
   print(f"| Connection Stub : {request.url}")
   print()
   print(f"-----------------------------------------------------------------------")

   return StreamingResponse(seeEventGenerator(topic="LINE_POST", request=request, redis_client=redis_client),media_type="text/event-stream",headers={"Cache-Control": "no-cache","Connection": "keep-alive", "X-Accel-Buffering": "no"})

