from models import Todos
from sqlmodel import Session
from database import engine

with Session(engine) as session:
    todo = Todos(
        title = "Fastapi",
        description = "lerning orms in Fastapi",
        completion = "False"
    )
session.add(todo)
session.commit()
session.refresh(todo)
