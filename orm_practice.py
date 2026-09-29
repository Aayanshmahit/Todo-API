from models import Todos
from sqlmodel import Session , select
from database import engine

#Create
with Session(engine) as session:
    todo = Todos(
        title = "Fastapi",
        description = "lerning orms in Fastapi",
        completion = False
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

#Read
    statement = select(Todos)
    execution = session.exec(statement)
    result = execution.all()

#Update
    todo = session.get(Todos , 1)
    todo.title = "Advanced concepts"
    todo.description = "I will take time to learn advanced concepts"
    todo.completion = False

    session.commit()

#Delete
    todo = session.get(Todos , 2)
    session.delete(todo)
    session.commit()