from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/jwt",
                   tags=["jwt"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

ALGORITHM: str = "HS256"
ACCESS_TOKEN_DURATION: int = 1
SECRET: str = "$2a$12$J1GfQnivl1396OWyPDH6GOU7KgT9IJIikeOY4.rerUwrnNlzMGWC."


oauth2 = OAuth2PasswordBearer(tokenUrl="login") # Le dice a FastAPI que los tokens se obtienen en la ruta "/login"

crypt = CryptContext(schemes=["bcrypt"]) # Algoritmo de encriptacion

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$p4YLREUzevde4fTWZnpzsu.GupJxCnYxhhBWGViqkONx6iVIzoffm",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$MvzoEiiLvvlTy5Qj21SQcuACTew.QHYoG41SPP/WJyqfNBdZ55SFy"
    }
}


async def auth_users(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
            raise exception
    return search_user(username)


async def current_user(user: User = Depends(auth_users)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # El ** desempaqueta el diccionario


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) # Obtiene los datos como diccionario
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_user_db(form.username) # Convierte los datos a un objeto UserDB
    if not crypt.verify(form.password, user.password): # Verifica si la contraseña del formulario es la misma que la contraseña encriptada en la DB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) # Tiempo actual mas el tiempo del token
    access_token = {
        "sub": user.username,
        "exp": expire,
        }
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user