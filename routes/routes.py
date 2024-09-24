import os
import base64
import requests
from fastapi import APIRouter, HTTPException, Path
from midtransclient import Snap
from models.models import ErrorResponse, PaymentData, create_transactions
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv(".env.dev")

# Load the environment variables
server_key = os.getenv("server_key")
payment_url = os.getenv("payment_url")
transaction_url = os.getenv("transaction_url")

# Validate environment variables
if not server_key:
    raise ValueError("The server_key environment variable must be set")
if not payment_url:
    raise ValueError("The payment_url environment variable must be set")
if not transaction_url:
    raise ValueError("The transaction_url environment variable must be set")

# Create a Snap MidTrans instance
snap = Snap(
    is_production=False,
    server_key=server_key,
)

# Initialize router
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)


@router.get("/")
async def health_check():
    """Returns a simple message to indicate the API is running."""
    return "Midtrans Payment Links API is running!"


def get_auth_string():
    """Generate the authorization string for Midtrans API."""
    return base64.b64encode(server_key.encode()).decode()


@router.post(
    "/v1/payment-links",
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_payment_url(payment_data: PaymentData):
    """Creates a payment link using Midtrans."""
    param = create_transactions(payment_data)

    try:
        transaction = snap.create_transaction(param)
        logging.info("Transaction Response: %s", transaction)
    except Exception as e:
        error_message = str(e)
        if "Duplicate order ID" in error_message:
            raise HTTPException(
                status_code=409,
                detail="Duplicate order ID. Order ID has already been utilized previously",
            )
        elif "Access denied" in error_message:
            raise HTTPException(
                status_code=401, detail="Access denied due to unauthorized request"
            )
        elif "Validation Error" in error_message or "Invalid JSON" in error_message:
            raise HTTPException(
                status_code=400, detail="Validation Error / Invalid JSON"
            )
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    transaction_token = transaction["token"]
    logging.info("Transaction Token: %s", transaction_token)

    return {
        "token": transaction_token,
        "redirect_url": f"{payment_url}/{transaction_token}",
    }


@router.get("/v1/{order_id}/status")
async def get_order_status(order_id: str = Path(...)):
    """Gets the status of an order."""
    url = f"{transaction_url}/{order_id}/status"
    auth_string = get_auth_string()
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {auth_string}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("Status Response: %s", response.json())
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

    response_data = response.json()
    response_data.pop("payment_amounts", None)  # remove payment_amounts if present

    return response_data
