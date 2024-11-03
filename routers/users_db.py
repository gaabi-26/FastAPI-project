from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
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
    return search_user_by_email(id)    


@router.get("/") 
async def user(id: int):
    return search_user_by_email(id)    


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if (type(search_user_by_email(user.email)) != User):
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")    

    user_dict = dict(user) # Transformar user en un diccionario
    del user_dict["id"] # Borrar el campo id para que mongoDB pueda generarla automaticamente
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id":id}))
    return User(**new_user)

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


def search_user_by_email(email: str):
    try:
        user = db_client.local.users.find_one({"email":email})
        return  user_schema(User(**user))
    except:
        return {"error":"User not found"}
