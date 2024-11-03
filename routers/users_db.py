from fastapi import APIRouter, HTTPException, status
from db.models.users import User
from db.client import db_client

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"detail":"Not found"}})


users_list = [User]


@router.get("/") 
async def users():
    return users_list


@router.get("/{id}") 
async def user(id: int):
    return search_users(id)    


@router.get("/") 
async def user(id: int):
    return search_users(id)    


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # if (type(search_users(user.id)) != User):
    #     users_list.append(user)
    #     return user

    user_dict = dict(user) # Transformar user en un diccionario
    del user_dict["id"] # Borrar el campo id para que mongoDB pueda generarla automaticamente
    db_client.local.user.insert_one(user_dict)

    return user

@router.put("/")
async def user(user: User):
    for index, user_saved in enumerate(users_list):
        if (user_saved.id == user.id):
            users_list[index] = user
            return users_list[index]
    return {"error":"User not found"}


@router.delete("/{id}") 
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
