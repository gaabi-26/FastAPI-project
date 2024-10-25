from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Inicia el server: uvicorn users:app --reload
# Detener el server: CTRL+C


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Gabriel", surname="Martinez", url="http//example.io", age="19"),
        User(id=2, name="Franco", surname="Colapinto", url="http//example.ar", age="19"),
        User(id=3, name="Alan", surname="Rodriguez", url="http//example.com", age="19"),]


# Url local: http://127.0.0.1:8000/users
@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}") # Path
async def user(id: int):
    return search_users(id)    


@app.get("/userquery/") # Query
async def user(id: int):
    return search_users(id)    


@app.post("/user/", status_code=201)
async def user(user: User):
    if (type(search_users(user.id)) != User):
        users_list.append(user)
        return user
    raise HTTPException(status_code=409, detail="User already exists")


@app.put("/user/")
async def user(user: User):
    for index, user_saved in enumerate(users_list):
        if (user_saved.id == user.id):
            users_list[index] = user
            return users_list[index]
    return {"error":"User not found"}


@app.delete("/user/{id}") # Path
async def user(id: int):
    for index, user_saved in enumerate(users_list):
        if (user_saved.id == id):
            user_deleted = users_list.pop(index)
            return user_deleted
    return {"error":"User not found"}


def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"User not found"}
