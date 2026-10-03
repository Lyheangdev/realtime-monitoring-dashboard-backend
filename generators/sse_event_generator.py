from fastapi import Request
from redis.asyncio import Redis
import asyncio
import time

async def seeEventGenerator(*,topic:str, request:Request, redis_client: Redis):
    pubsub = redis_client.pubsub()

    # subscribe to a specific channel
    await pubsub.subscribe(topic)

    last_ping = time.monotonic()

    try:
        while True:
                
        # Check request connection
            if await request.is_disconnected():
                break

            message = await pubsub.get_message(ignore_subscribe_messages=True)
                
            if message:
                data = message["data"]
                last_ping = time.monotonic()

                yield f"data: {data}\n\n"

            elif time.monotonic() - last_ping > 10:
                print(f"[ SSE ping to client : Agent:{request.headers.get("user-agant")} - {request.client.host}:{request.client.port} to keep connection alive! ]")
                yield ": ping\n\n"
                last_ping = time.monotonic()

            else:
                await asyncio.sleep(0.1)

    finally:
        print(f"[ Agent:{request.headers.get("user-agant")} - {request.client.host}:{request.client.port}  is disconnected ! ]")
        await pubsub.unsubscribe(topic)
        await pubsub.close()