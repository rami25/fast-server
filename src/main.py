from fastapi import FastAPI
from .api import routes

app = FastAPI()

routes(app)
