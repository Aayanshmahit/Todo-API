from fastapi import FastAPI , HTTPException
from validate import ValidInputs
from patch_validation import patch_input_validate
from database import get_connection
import sqlite3
from models import Todos
from database import get_session
from sqlmodel import Session , select
from fastapi import Depends
from database import engine
from sqlmodel import Field , SQLModel

app = FastAPI()

@app.post("/posts")
def create_post(data : ValidInputs , session : Session = Depends(get_session)):
    todo = Todos(
        title = data.title,
        description = data.description,
        completion = data.completion
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return session.get(Todos , todo.id)

@app.get("/posts")
def get_post(session : Session = Depends(get_session)):
    statement = select(Todos)
    result = session.exec(statement)
    rows = result.all()
    return rows

@app.get("/posts/{id}")
def get_post_id(id : int):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM todos where id = ?""",(id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code = 404 , detail = "Post not Found")
    except sqlite3.Error:
        raise HTTPException(status_code = 500 , detail = "Database error")

    finally:
        connection.close()
    return row

@app.delete("/posts/{id}")
def delete_post(id : int):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""DELETE FROM todos where id = ?""",(id,))
        deleted = cursor.rowcount
        if deleted == 0:
            raise HTTPException(status_code = 404 , detail = "Post not Found")
        connection.commit()

    except sqlite3.Error:
        raise HTTPException(status_code = 500 , detail = "Database error")

    finally:
        connection.close()
    
    return "Post Deleted successfully"

@app.put("/posts/{id}")
def update_post(id : int , data : ValidInputs):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""UPDATE todos set "title" = ? , "description" = ? , completion = ? where id = ?""",(data.title,data.description,data.completed,id,))

        update = cursor.rowcount
        if update == 0:
            raise HTTPException(status_code = 404 , detail = "Post not Found")
        connection.commit()
        
        cursor.execute("""SELECT * FROM todos where id = ?""",(id,))
        rows = cursor.fetchone()
    except sqlite3.Error:
        raise HTTPException(status_code = 500 , detail = "Database error")

    finally:
        connection.close()
    return rows

@app.patch("/posts/{id}")
def update_value_post(id : int , data : patch_input_validate):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        if data.title is not None:
            cursor.execute("""UPDATE todos SET title = ? WHERE id = ?""",(data.title , id,))

        if data.description is not None:
            cursor.execute("""UPDATE todos SET description = ? WHERE id = ?""",(data.description , id,))

        if data.completed is not None:
            cursor.execute("""UPDATE todos SET completion = ? WHERE id = ?""",(data.completed , id,))

        connection.commit()
        cursor.execute("""SELECT * FROM todos WHERE id = ? """,(id,))
        rows = cursor.fetchone()

        if rows is None:
            raise HTTPException(status_code = 404 , detail = "Post not Found")

    except sqlite3.Error:
            raise HTTPException(status_code = 500 , detail = "Database error")

    finally:
        connection.close()

    return rows