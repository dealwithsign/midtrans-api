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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan akses dari semua domain
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode HTTP (GET, POST, PUT, DELETE, dll.)
    allow_headers=["*"],  # Mengizinkan semua header
)


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    start_time = datetime.now()
    response: Response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    logging.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time}s")
    return response

# Error handling middleware
@app.middleware("http")
async def add_error_handling(request: Request, call_next: Callable):
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            logging.error(f"Error: {response.status_code} - {response.body.decode()}")
        return response
    except Exception as e:
        logging.error(f"Unhandled Exception: {str(e)}")
        return Response("Internal Server Error", status_code=500)

app.include_router(router)


