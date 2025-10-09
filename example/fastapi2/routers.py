from fastapi import APIRouter, HTTPException, Depends
from database import UserRepository as ur
from shemas import *


default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags = ["Пользователи"]
)

quizes_router = APIRouter(
    prefix="/quizes",
    tags = ["Квизы"]
)

@default_router.get('/', tags=['API V1'])
async def index():
    
    return {'data':'ok'}


# ответ в виде одиночного списка
@users_router.get('')
async def users_get() -> list[User]:  
    users =   await ur.get_users()
    return users

# с развернутым ответом 
@users_router.get('/u2')
async def users_get2() -> dict[str, list[User] | str]: 
    users =   await ur.get_users()
    return {'status':'ok', 'data':users}


    


@users_router.get('/{id}')
async def user_get(id: int) -> User :  
    user =   await ur.get_user(id)
    if user:
        return user    
    raise HTTPException(status_code=404, detail="User not found")
    # или return {'err':"User not found, ..."} # но тогда get_user(id) -> User | dict[str,str]


@users_router.post('')
async def add_user(user:UserAdd = Depends()) -> UserId:
# async def add_user(user:UserAdd) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}


@quizes_router.get('')
def index():
    return {'data':'quizes'}
    

