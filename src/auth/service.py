from datetime import timedelta, datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import Depends
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from . import models
from . import models1
from ..exceptions import AuthenticationError
from ..database.main import DB
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import logging

from fastapi.concurrency import run_in_threadpool



# You would want to store this in an environment variable or a secret manager
SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# i will define them as tools
def verify_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
  return bcrypt_context.hash(password)


# token
def create_access_token(name: str, user_id: str, expires_delta: timedelta) -> str:
  encode = {
    'sub': name,
    'id': user_id,
    'exp': datetime.now(timezone.utc) + expires_delta
  }
  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# def verify_token(token: str) -> models.TokenData:
#   try:
#     payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
#     user_id: str = payload.get('id')
#     return models.TokenData(user_id=user_id)
#   except PyJWTError as e:
#     logging.warning(f"Token verification failed: {str(e)}")
#     raise AuthenticationError()

# def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:
#     return verify_token(token)

async def register_user(db, user: models1.RegisterUserRequest) -> models1.RegisterUserResponse:
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    result = await run_in_threadpool(db["users"].insert_one, user_dict)
    created = await run_in_threadpool(db["users"].find_one, {"_id": result.inserted_id})
    return models1.RegisterUserResponse(
        id=str(created["_id"]),
        first_name=created["first_name"],
        last_name=created["last_name"],
        email=created["email"],
        role=created["role"],
    )

# async def authenticate_user(db, data: models1.SignUserRequest) -> models1.SignUserResponse:
async def authenticate_user(db, data: models1.SignUserRequest) -> dict | None:
    query = {
        "$or": [
            {"first_name": data.login},
            {"email": data.login}
        ]
    }
    user = await run_in_threadpool(db["users"].find_one, query)
    if not user:
      return None
    if not verify_password(data.password, user.get("password")):
      return None
    return user

async def login_user(db, data: models1.SignUserRequest) -> models1.SignUserResponse:
  user = await authenticate_user(db, data)
  if not user:
    return None
  _token = create_access_token(user["first_name"], str(user["_id"]), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  return models1.SignUserResponse(
      id=str(user["_id"]),
      first_name=user["first_name"],
      last_name=user["last_name"],
      email=user["email"],
      role=user["role"],
      token=models1.Token(
        access_token=_token,
        token_type='bearer'
      )
  )
    


def get_current_user():
  pass