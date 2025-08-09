from fastapi import FastAPI
# from src.users.controller import router as users_router
from src.auth.controller import router as auth_router

def routes(app: FastAPI):
    # app.include_router(users_router)
    app.include_router(auth_router)