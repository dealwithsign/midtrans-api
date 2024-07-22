import os
from fastapi import FastAPI, HTTPException, Path, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from routes.routes import router
import logging
import sys
import time
from datetime import datetime
from typing import Any, Callable, TypeVar

description = """
This is a fancy API built with [FastAPI🚀](https://fastapi.tiangolo.com/)

📝 [Source Code](https://github.com/dpills/fastapi-prod-guide)  
🐞 [Issues](https://github.com/dpills/fastapi-prod-guide/issues) 
"""

app = FastAPI(
    title="Midtrans Payment Links API - Rental Mobil",
    description=" api for create payment and get transaction status",
    version="1.0.0",
    docs_url="/",
    
    
)

# cross middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)

app.include_router(router)
