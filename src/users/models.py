from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import dateime

class UserResponse(BaseModel):
  id: UUID
  first_name: str
  last_name: str
  email: EmailStr
  role: int

class PasswrodChange(BaseModel):
  current_password: str
  new_password: str
  new_password_confirm: str
