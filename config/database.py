from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, DeclarativeBase
from fastapi  import Depends
from typing import Annotated

"""
@Description: SQLAlchemy base model
"""
class BaseModel(DeclarativeBase):
    pass


"""
 @Description: postgres connection set up
"""
class PostGresConnector:
    HOST='localhost'
    PORT=5432
    USERNAME='minghua'
    PASSWORD='progres_test'
    INITIAL_DATABASE='dashboard_tst'

    CONNECTION_STRING = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{INITIAL_DATABASE}'

    # Initial Sqlalchemy engine
    def __init__(self):
        self.engine = create_engine(url=self.CONNECTION_STRING, echo=True)

    # Reuse connector engine
    def getConnector(self) -> Engine:
        return self.engine

    # Reuse session
    def getSession(self):
        with Session(self.engine) as session:
            yield session

    # Reuse dependancy
    def getSessionDependacy(self):
        session_deps = Annotated[Session, Depends(self.getSession)]
        return session_deps