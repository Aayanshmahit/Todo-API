from fastapi import FastAPI , HTTPException
from validate import ValidInputs
from patch_validation import patch_input_validate
from database import get_session
from models import Todos
from database import get_session
from sqlmodel import Session , select , or_
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
def get_post(limit_no : Optional[int] = None , offset_no : Optional[int] = None , sort_by : Optional[str] = None , order_by : Optional[str] = None , search : Optional[str] = None , completed : Optional[bool] = None , session : Session = Depends(get_session)):

    statement = select(Todos)

    if limit_no is not None and limit_no <= 0 :
        raise HTTPException(status_code = 400 , detail = "invalid values")

    if offset_no is not None and offset_no < 0:
        raise HTTPException(status_code = 400 , detail = "invalid values")

    if limit_no is not None:
        statement = statement.limit(limit_no)

    if offset_no is not None:
        statement = statement.offset(offset_no)

    if (sort_by is None) != (order_by is None):
        raise HTTPException(
            status_code=400,
            detail="sort_by and order_by must be provided together"
        )

    columns = {
        "id": Todos.id,
        "title": Todos.title
    }

    if sort_by is not None:
        if sort_by not in columns:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")

        if order_by not in ("asc", "desc"):
            raise HTTPException(
                status_code=400,
                detail="order_by must be 'asc' or 'desc'"
            )

    if sort_by is not None:
        column = columns[sort_by]
        statement = statement.order_by(
            column.asc() if order_by == "asc" else column.desc()
        )

    if completed is not None:
        statement = statement.where(Todos.completion == completed)

    if search is not None:
        statement = statement.where(
        or_
        (Todos.title.contains(search) , Todos.description.contains(search))
        )

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