from sqlmodel import SQLModel , create_engine
from models import Todos

engine = create_engine("sqlite:///todos.db")

SQLModel.metadata.create_all(engine)