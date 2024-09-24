from typing import List
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta


class Booking(BaseModel):
    id: str
    carId: str
    carName: str
    selectedDate: datetime
    selectedTime: str
    selectedPassengers: int
    selectedLocationPick: str
    selectedLocationDrop: str
    carFrom: str
    carTo: str
    carDate: datetime
    userId: str
    userName: str
    userPhone: str
    userEmail: str
    isPayment: bool
    totalPayment: int


# Error response model
class ErrorResponse(BaseModel):
    detail: str


# Item detail model
class ItemDetail(BaseModel):
    id: str
    name: str
    price: int
    quantity: int


# Customer detail model
class CustomerDetail(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    notes: str


# Expiry model
class Expiry(BaseModel):
    duration: int
    unit: str


# Transaction detail model
class TransactionDetail(BaseModel):
    order_id: str
    gross_amount: int
    payment_link_id: str


# Payment data model
class PaymentData(BaseModel):
    transaction_details: TransactionDetail
    credit_card: dict
    usage_limit: int
    expiry: Expiry
    item_details: List[ItemDetail]
    customer_details: CustomerDetail


# Function to build transaction parameters
def create_transactions(payment_data: PaymentData):
    """Builds the transaction parameters from the payment data."""
    return {
        "transaction_details": {
            "order_id": payment_data.transaction_details.order_id,
            "gross_amount": payment_data.transaction_details.gross_amount,
        },
        "credit_card": {"secure": payment_data.credit_card["secure"]},
        "customer_details": {
            "first_name": payment_data.customer_details.first_name,
            "last_name": payment_data.customer_details.last_name,
            "email": payment_data.customer_details.email,
            "phone": payment_data.customer_details.phone,
        },
        "expiry": {
            "start_time": datetime.now(timezone(timedelta(hours=7))).strftime(
                "%Y-%m-%d %H:%M:%S %z"
            ),
            "duration": payment_data.expiry.duration,
            "unit": payment_data.expiry.unit,
        },
        "item_details": [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
            }
            for item in payment_data.item_details
        ],
    }
