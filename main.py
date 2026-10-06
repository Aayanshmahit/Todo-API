from fastapi import FastAPI , HTTPException
from validate import ValidInputs
from patch_validation import patch_input_validate
from database import get_session
from models import Todos
from database import get_session
from sqlmodel import Session , select
from fastapi import Depends
from typing import Optional

app = FastAPI()

@app.post("/posts")
def create_post(data : ValidInputs , session : Session = Depends(get_session)):
    todo = Todos(
        title = data.title,
        description = data.description,
        completion = data.completed
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return session.get(Todos , todo.id)

@app.get("/posts")
def get_post(search : Optional[str] = None , completed : Optional[bool] = None , session : Session = Depends(get_session)):

    if completed is None:
        statement = select(Todos)
    else:
        statement = select(Todos).where(Todos.completion == completed)

    if search is None:
        statement = select(Todos)
    else:
        statement = select(Todos).where(Todos.title and Todos.description == search)

    result = session.exec(statement)
    return result.all()

@app.get("/posts/{id}")
def get_post_id(id : int , session : Session = Depends(get_session)):

    todo = session.get(Todos , id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return todo

@app.delete("/posts/{id}")
def delete_post(id : int , session : Session = Depends(get_session)):
    todo = session.get(Todos , id)
    if todo is None:
        raise HTTPException(status_code = 404 , detail = "Post not found")
    session.delete(todo)
    session.commit()
    
    return "Post Deleted successfully"

@app.put("/posts/{id}")
def update_post(id : int , data : ValidInputs , session : Session = Depends(get_session)):

    todo = session.get(Todos , id)
    if todo is None:
        raise HTTPException(status_code =404 , detail = "todo not found")

    todo.title = data.title
    todo.description = data.description
    todo.completion = data.completed

    session.commit()
    return todo

@app.patch("/posts/{id}")
def update_value_post(id : int , data : patch_input_validate , session :  Session = Depends(get_session)):

    todo = session.get(Todos , id)

    if todo is None:
        raise HTTPException(status_code = 404 , detail = "Post not found")

    if data.title is not None:
        todo.title = data.title

    if data.description is not None:
        todo.description = data.description

    if data.completed is not None:
        todo.description = data.description

    session.commit()

    return todo