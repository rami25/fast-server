from . import models
from ..auth import service, models as auth_models

from typing import Annotated
from fastapi import Depends
from ..exceptions import AuthenticationError
from bson import ObjectId

from fastapi.concurrency import run_in_threadpool

async def get_user_by_id(db, user) -> models.User | None:
  try:
    return await run_in_threadpool(db["users"].find_one, {"_id": ObjectId(user.get_id())})
  except Exception:
    return None
    raise HTTPException(status_code=400, detail="Invalid user ID")

async def add_user(db, new_user: models.User, _user: auth_models.TokenData) -> models.User | dict:
  user = await get_user_by_id(db, _user)
  if user and user.get('role') == 1:
    await service.register_user(db, new_user)
  else:
    return {'msg' : 'failed'}

async def update_user(db, new_user: models.Userupd, _user:auth_models.TokenData) -> models.Userupd:
  user = await get_user_by_id(db, _user)
  if user and user.get('role') == 1:
    await service.register_user(db, new_user)
  else:
    return {'msg' : 'failed'}
  pass

async def delete_user(user_id):
  pass