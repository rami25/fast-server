from fastapi import APIRouter, Depends, status
from ..auth import auth, models as auth_models
from . import service, models
from ..database.main import DB

router = APIRouter(
  prefix="/forms",
  tags=["forms"]
)

@router.post("/add_form")
async def add_form(db: DB, form: models.Form, user : auth_models.TokenData = Depends(auth.get_current_user)) -> models.FormResponse | dict:
  return await service.add_form(db, form, user)

@router.patch("/update_form")
async def update_form(db: DB, form: models.UpdateForm, user : auth_models.TokenData = Depends(auth.get_current_user)) -> models.FormResponse | dict:
  return await service.update_form(db, form, user)

@router.delete("/delete_form")
async def delete_form(db: DB, form: models.DeleteForm, user : auth_models.TokenData = Depends(auth.get_current_user)) -> dict:
  return await service.delete_form(db, form, user) 