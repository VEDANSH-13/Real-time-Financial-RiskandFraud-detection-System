"""
Pydantic schemas for transactions.
"""

from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from models.transaction import TransactionType, TransactionStatus


class TransactionCreate(BaseModel):
    """Schema for creating a new transaction."""
    amount: float = Field(..., gt=0, description="Transaction amount")
    transaction_type: TransactionType = Field(..., description="credit or debit")
    location: Optional[str] = Field(None, description="Location of transaction")
    # For simulation, simulator will optionally provide status or user_id
    # Default APIs will extract user_id from token.


class TransactionResponse(BaseModel):
    """Schema for a transaction in responses."""
    id: UUID
    user_id: UUID
    amount: float
    transaction_type: TransactionType
    timestamp: datetime
    location: Optional[str]
    status: TransactionStatus
    is_fraud: bool
    anomaly_score: float

    class Config:
        from_attributes = True
