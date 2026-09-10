from fastapi import FastAPI , HTTPException
from validate import ValidInputs
from patch_validation import patch_input_validate

app = FastAPI()

post_num = 1
post_store = {}

@app.post("/posts")
def create_post(data : ValidInputs):
    global post_num
    response = {
        "title" : data.title , 
        "description" : data.description,
        "completion" : data.completed
    }
    post_store[post_num] = response
    post_num+=1
    return response

@app.get("/posts")
def get_post():
    return post_store

@app.get("/posts/{id}")
def get_post_id(id : int):
    if id not in post_store:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    return post_store.get(id)

@app.delete("/posts/{id}")
def delete_post(id : int):
    if id not in post_store:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    del post_store[id]
    return "Post deleted sucessfully"
    

@app.put("/posts/{id}")
def update_post(id : int , data : ValidInputs):
    if id not in post_store:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    post_store[id] = {
        "title" : data.title , 
        "description" : data.description,
        "completion" : data.completed
    }
    return post_store[id]

@app.patch("/posts/{id}")
def update_single_post(id : int , data : patch_input_validate):
    if id not in post_store:
        raise HTTPException(status_code = 404 , detail = "Post not Found")
    post_store[id] = {
        "title" : data.title if data.title is not None else post_store[id]["title"],
        "description" : data.description if data.description is not None else post_store[id]["description"],
        "completion" : data.completed if data.completed is not None else post_store[id]["completion"]
    }
    return post_store[id]