import logging
from datetime import datetime
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.routes import router

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="Lalan Midtrans Payment API",
    description="API for processing payments and retrieving transaction statuses in the Lalan app",
    version="1.0.0",
    docs_url="/",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow access from all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    start_time = datetime.now()
    response: Response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    logging.info(
        f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time}s"
    )
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


# Include router
app.include_router(router)
