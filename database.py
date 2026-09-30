from sqlmodel import SQLModel , create_engine , Session
from models import Todos

engine = create_engine("sqlite:///todos.db")

SQLModel.metadata.create_all(engine)

# Session dependency
def get_session():
    with Session(engine) as session:
        yield session