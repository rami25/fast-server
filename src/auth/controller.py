from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import  models
from . import service
from . import auth
from fastapi.security import OAuth2PasswordRequestForm
from ..database.main import DB
# from ..rate_limiter import limiter

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db: DB, user: models.RegisterUserRequest) -> models.RegisterUserResponse | dict:
  new_user = await service.register_user(db, user)
  return new_user


@router.get("/login") #, response_model=models.Token)
async def login_user(db: DB, data: models.SignUserRequest | dict) -> models.SignUserResponse | dict:#Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await service.login_user(db, data)


# @router.post("/add_user")
# async def add_user(db: DB, new_user: models.RegisterUserRequest, user : models.TokenData = Depends(auth.get_current_user)) -> models.RegisterUserRequest | dict:
#   return await service.add_user(db, new_user, user)

# @router.put("/update_user")
# async def update_user(db: DB, new_user: models.RegisterUserRequest, user : models.TokenData = Depends(auth.get_current_user)) -> models.RegisterUserRequest | dict:
#   return await service.add_user(db, new_user, user)

# @router.delete("/delete_user")
# async def delete_user(db: DB, new_user: models.RegisterUserRequest, user : models.TokenData = Depends(auth.get_current_user)) -> models.RegisterUserRequest | dict:
#   return await service.add_user(db, new_user, user)