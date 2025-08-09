from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from fastapi.concurrency import run_in_threadpool

# You would want to store this in an environment variable or a secret manager
SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')