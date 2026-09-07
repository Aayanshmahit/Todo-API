from fastapi import FastAPI , HTTPException
from validate import ValidInputs

app = FastAPI()

post_num = 0
post_store = {}

@app.post("/posts")
def create_post(data : ValidInputs):
    global post_num
    response = {
        "id" : post_num+1 ,
        "title" : data.title , 
        "description" : data.description,
        "completion" : data.completed
    }
    post_num+=1
    post_store[post_num] = response
    return response

@app.get("/posts")
def get_post():
    return post_store

@app.get("/posts/{id}")
def get_post_id():
    pass

@app.delete("/posts")
def delete_post():
    pass

@app.put("/posts/{id}")
def update_post():
    pass