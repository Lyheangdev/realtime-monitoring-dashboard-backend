from contextlib import asynccontextmanager
from .websocket import SocketManager
from .database  import PostGresConnector, BaseModel
from .redis import RedisConnector

# Application modules
from ..router.line import router as lineRouter
from ..router.user import router as userRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize configuration instances
socketManager = SocketManager()
databaseManager = PostGresConnector()

@asynccontextmanager
async def preConfiguration(app: FastAPI):
    # Load | Configure | Boostrapt something before FastApi instance is ready to serve for any others service
    sqlAlchemy_engine = databaseManager.getConnector()
    BaseModel.metadata.create_all(sqlAlchemy_engine)

    redisInitializer = RedisConnector()

    yield
    # post-excute code before FastApi service completely shutdown
    redisInitializer.redis_client.close()


app = FastAPI(lifespan=preConfiguration)

allowed_origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register router
root_path_prefix_v1 = "/api/v1"
app.include_router(router=lineRouter, prefix=root_path_prefix_v1)
app.include_router(router=userRouter, prefix=root_path_prefix_v1)
