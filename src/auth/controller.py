from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import  models
from . import  models1
from . import service
from fastapi.security import OAuth2PasswordRequestForm
from ..database.main import get_db, DB
# from ..rate_limiter import limiter

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: models1.RegisterUserRequest, db: DB) -> models1.RegisterUserResponse:
  new_user = await service.register_user(db, user)
  return new_user


@router.get("/login") #, response_model=models.Token)
async def login_for_access_token(db: DB, data: models1.SignUserRequest) -> models1.SignUserResponse:#Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await service.login_user(db, data)