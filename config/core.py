from contextlib import asynccontextmanager
from .websocket import SocketManager
from .database  import PostGresConnector, BaseModel


from fastapi import FastAPI

# Initialize configuration instances
socketManager = SocketManager()
databaseManager = PostGresConnector()


@asynccontextmanager
async def preConfiguration(app: FastAPI):
    # Load | Configure | Boostrapt something before FastApi instance is ready to serve for any others service
    sqlAlchemy_engine = databaseManager.getConnector()
    BaseModel.metadata.create_all(sqlAlchemy_engine)

    yield

    # post-excute code before FastApi service completely shutdown


app = FastAPI(lifespan=preConfiguration)