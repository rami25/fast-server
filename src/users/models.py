from pydantic import BaseModel, EmailStr
from ..auth import models

class User(models.RegisterUserRequest):
  pass

class UpdateUserRequest(models.RegisterUserResponse):
  pass

class DeleteUserRequest(BaseModel):
  id: str


class UserResponse(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  role: int

class PasswrodChange(BaseModel):
  current_password: str
  new_password: str
  new_password_confirm: str
