"""
Transaction model for the fintech system.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
import enum


class TransactionType(str, enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionStatus(str, enum.Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    SUSPICIOUS = "suspicious"
    FLAGGED = "flagged"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    location = Column(String(255), nullable=True)
    status = Column(
        SQLEnum(TransactionStatus),
        default=TransactionStatus.COMPLETED,
        nullable=False,
        index=True,
    )
    is_fraud = Column(Boolean, default=False, nullable=False, index=True)
    anomaly_score = Column(Float, default=0.0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, is_fraud={self.is_fraud})>"
