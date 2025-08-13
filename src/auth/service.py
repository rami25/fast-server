from typing import Annotated
from fastapi import Depends
from . import models, auth
from ..exceptions import AuthenticationError
from bson import ObjectId

from fastapi.concurrency import run_in_threadpool

async def register_user(db, user: models.RegisterUserRequest) -> models.RegisterUserResponse | dict:
  try:
    user_dict = user.dict()
    user_dict["password"] = auth.hash_password(user.password)
    result = await run_in_threadpool(db["users"].insert_one, user_dict)
    created = await run_in_threadpool(db["users"].find_one, {"_id": result.inserted_id})
    return models.RegisterUserResponse(
        id=str(created["_id"]),
        first_name=created["first_name"],
        last_name=created["last_name"],
        email=created["email"],
        role=created["role"],
    )
  except Exception as e:
    return { 'msg' : f'Failed to register user. {str(e)}' }

async def authenticate_user(db, data: models.SignUserRequest | dict) -> models.SignUserResponse | None:
    query = {
        "$or": [
            {"first_name": data.login},
            {"email": data.login}
        ]
    }
    user = await run_in_threadpool(db["users"].find_one, query)
    if not user:
      return None
    if not auth.verify_password(data.password, user.get("password")):
      return None
    return user

async def login_user(db, data: models.SignUserRequest | dict) -> models.SignUserResponse | dict:
  user = await authenticate_user(db, data)
  if not user:
    return { 'msg' : 'failed' }
  _token = auth.create_access_token(user["first_name"], str(user["_id"]))
  return models.SignUserResponse(
      id=str(user["_id"]),
      first_name=user["first_name"],
      last_name=user["last_name"],
      email=user["email"],
      role=user["role"],
      token=models.Token(
        access_token=_token,
        token_type='bearer'
      )
  )