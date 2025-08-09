from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterUserRequest(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  password: str
  role: int

class RegisterUserResponse(BaseModel):
  id: str
  first_name: str
  last_name: str
  email: EmailStr
  role: int

class SignUserRequest(BaseModel):
  login: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class SignUserResponse(RegisterUserResponse):
  token: Token