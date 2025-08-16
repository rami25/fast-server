from fastapi import FastAPI
from src.auth.controller import router as auth_router
from src.users.controller import router as users_router
from src.form.controller import router as forms_router

def routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(forms_router)