# from uuid import UUID
# from pydantic import BaseModel, EmailStr

# class RegisterUserRequest(BaseModel):
#   first_name: str
#   last_name: str
#   email: EmailStr
#   password: str
#   role: int

# class Token(BaseModel):
#   access_token: str
#   token_type: str

# class TokenData(BaseModel):
#   user_id: str | None = None

#   def get__uuid(self) -> UUID | None:
#     if self.user_id:
#       return UUID(self.user_id)
#     return None

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Custom ObjectId type for Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Request model (no id here, MongoDB generates it)
class User(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    password: str
    role: int

# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data model (user_id now supports ObjectId)
class TokenData(BaseModel):
    # user_id: Optional[str] = None
    user_id: str | None = None

    def get_object_id(self) -> Optional[ObjectId]:
        return self.user_id





####################
# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from bson import ObjectId

# # Base model with common fields
# class UserBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     role: int

# # For creating a new user (password is included)
# class UserIn(UserBase):
#     password: str

# # For storing in DB (MongoDB ObjectId, hashed password)
# class UserDB(UserBase):
#     id: Optional[str]  # MongoDB ObjectId as string
#     hashed_password: str

# # For returning to clients (no password)
# class UserOut(UserBase):
#     id: str
