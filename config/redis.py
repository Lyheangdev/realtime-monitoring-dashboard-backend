from fastapi import Depends
from redis.asyncio import Redis
from typing import Annotated
from datetime import datetime
import sys

"""
@Description: Redis service connection setup !
"""
class RedisConnector:
    HOST="localhost"
    PORT=6379
    PASSWORD="sviaec_dashboard"
    DECODE_RESPONSE=True

    __redis_instance= None

    def __new__(cls):
        if cls.__redis_instance is None:
            cls.__redis_instance = super().__new__(cls)
        return cls.__redis_instance

    def __init__(self):
        # Check whether redis client hasn't initialize
        if hasattr(self, "redis_client"):
            return
        
        self.redis_client = Redis(
            host=self.HOST,
            port=self.PORT,
            password=self.PASSWORD,
            decode_responses=self.DECODE_RESPONSE
        )

        print(f"-------------   | REDIS SERVICE CONNECTION IS SET UP | ----------------")
        print()
        print(f"| Established at: {datetime.now()}")
        print(f"| Run by: PYTHON {sys.version}")
        print()
        print(f"-----------------------------------------------------------------------")

    def get_redis_client(self):
        return self.redis_client

    @classmethod
    def get_redis_instance(cls):
        return cls.__redis_instance

    async def close_service(self):
        if self.__redis_instance is None:
            return
        
        await self.redis_client.aclose()


# Redis client dependency
def redis_client_depend():
    redis = RedisConnector.get_redis_instance()
    try:
        yield redis.redis_client

    except Exception as e:
        raise e


# External use for redis client path operation function injection
redisClientDepend = Annotated[Redis, Depends(redis_client_depend)]