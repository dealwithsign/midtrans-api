import os
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.routes import router



app = FastAPI()
app.include_router(router)
