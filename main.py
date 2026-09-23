from fastapi import FastAPI , HTTPException
from validate import ValidInputs
from patch_validation import patch_input_validate
from database import get_connection
import sqlite3

app = FastAPI()

@app.post("/posts")
def create_post(data : ValidInputs):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO todos(title,description,completion)
            VALUES(? , ? , ?)
        """,(data.title , data.description , data.completed))
        connection.commit()

        new_row = cursor.lastrowid
        cursor.execute("""SELECT * FROM todos where id = ?""",(new_row,))
        row = cursor.fetchone()

    except sqlite3.Error:
        raise HTTPException(status_code = 500 , detail = "Database Error")

    finally:
        connection.close()
        return row

@app.get("/posts")
def get_post():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM todos""")
    rows = cursor.fetchall()
    return rows

@app.get("/posts/{id}")
def get_post_id(id : int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM todos where id = ?""",(id,))
    rows = cursor.fetchone()

    if not rows:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    return rows

@app.delete("/posts/{id}")
def delete_post(id : int):
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM todos where id = ?""",(id,))
    deleted = cursor.rowcount
    if deleted == 0:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    connection.commit()
    
    return deleted

@app.put("/posts/{id}")
def update_post(id : int , data : ValidInputs):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""UPDATE todos set "title" = ? , "description" = ? , completion = ? where id = ?""",(data.title,data.description,data.completed,id,))

    update = cursor.rowcount
    if update == 0:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    connection.commit()
    
    cursor.execute("""SELECT * FROM todos where id = ?""",(id,))
    rows = cursor.fetchall()
    return rows

@app.patch("/posts/{id}")
def update_value_post(id : int , data : patch_input_validate):
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

    return rows