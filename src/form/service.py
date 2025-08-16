from . import models
from ..auth import service as auth_service, models as auth_models
from ..users import service as user_service

from typing import Annotated
from fastapi import Depends, HTTPException
from ..exceptions import AuthenticationError
from bson import ObjectId

from fastapi.concurrency import run_in_threadpool

async def add_form_util(db, form):
  try:
    form_dict = form.dict()
    ret = await run_in_threadpool(db["forms"].insert_one, form_dict)
    created = await run_in_threadpool(db["forms"].find_one, {"_id": ret.inserted_id})
    return models.FormResponse(
        id=str(created["_id"]),
        questions=created["questions"]
    )
  except Exception as e:
    return { 'msg' : f'Failed to add form. {str(e)}' }
  
async def add_form(db, form, user):
  user = await user_service.get_user_by_id(db, user)
  if user and user.get('role') == 1:
    return await add_form_util(db, form)
  else:
    return {'msg' : 'failed'}

async def update_form_util(db, form):
  if not ObjectId.is_valid(form.id):
    raise HTTPException(status_code=400, detail="Invalid form ID")

  update_dict = {k: v for k, v in form.dict().items() if k != "id" and v is not None}

  if not update_dict:
      raise HTTPException(status_code=400, detail="No fields to update")

  result = await run_in_threadpool(
      db["forms"].update_one,
      {"_id": ObjectId(form.id)},
      {"$set": update_dict}
  )

  if result.matched_count == 0:
      raise HTTPException(status_code=404, detail="Form not found")

  ret = await run_in_threadpool(db["forms"].find_one, {"_id": ObjectId(form.id)})
  ret["_id"] = str(ret["_id"])
  return ret
  # return {"message": "User updated successfully"}
  
async def update_form(db, form, user):
  user = await user_service.get_user_by_id(db, user)
  if user and user.get('role') == 1:
    return await update_form_util(db, form)
  else:
    return {'msg' : 'failed'}

async def delete_form_util(db, form):
  if not ObjectId.is_valid(form.id):
      raise HTTPException(status_code=400, detail="Invalid form ID")

  result = await run_in_threadpool(
      db["forms"].delete_one,
      {"_id": ObjectId(form.id)}
  )

  if result.deleted_count == 0:
      raise HTTPException(status_code=404, detail="Form not found")

  return {"message": "Form deleted successfully"}
  
async def delete_form(db, form, user):
  user = await user_service.get_user_by_id(db, user)
  if user and user.get('role') == 1:
    return await delete_form_util(db, form)
  else:
    return {'msg' : 'failed'}

async def evaluate_form_util(db, form):
  pass
async def evaluate_form(db, form, user):
  user = await user_service.get_user_by_id(db, user)
  if user and user.get('role') == 1:
    return await add_form_util(db, form)
  else:
    return {'msg' : 'failed'}
