from pydantic import BaseModel, EmailStr
from ..auth import models

class User(models.RegisterUserRequest):
  pass

class Userupd(models.RegisterUserResponse):
  pass

class UserResponse(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  role: int

class PasswrodChange(BaseModel):
  current_password: str
  new_password: str
  new_password_confirm: str
