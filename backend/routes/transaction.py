"""
Transaction routes and WebSocket broadcasting.
"""

from fastapi import APIRouter, Depends, status, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict
from uuid import UUID

from config.database import get_db
from models.user import User
from models.transaction import Transaction, TransactionStatus
from schemas.transaction import TransactionCreate, TransactionResponse
from services.auth_service import get_current_user, AuthService

import json
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Custom JSON encoder to handle UUIDs and Dates for websockets
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "value"): # For Enums
            return obj.value
        return super().default(obj)

class ConnectionManager:
    """Manages active WebSocket connections per user."""
    def __init__(self):
        # user_id -> list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

manager = ConnectionManager()


from services.fraud_service import fraud_engine

@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
)
async def create_transaction(
    tx_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction for the current user. Evaluates Fraud Logic.
    """
    # Fetch recent transactions for velocity rules
    recent_txs = db.query(Transaction)\
                   .filter(Transaction.user_id == current_user.id)\
                   .order_by(desc(Transaction.timestamp))\
                   .limit(10)\
                   .all()

    # Evaluate using ML & Rules
    is_fraud, anomaly_score = fraud_engine.evaluate_transaction(tx_data.amount, recent_txs)

    status_val = TransactionStatus.SUSPICIOUS if is_fraud else TransactionStatus.COMPLETED

    db_tx = Transaction(
        user_id=current_user.id,
        amount=tx_data.amount,
        transaction_type=tx_data.transaction_type,
        location=tx_data.location,
        status=status_val,
        is_fraud=is_fraud,
        anomaly_score=anomaly_score
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)

    # Broadcast to active user's dashboard!
    tx_dict = {
        "id": str(db_tx.id),
        "user_id": str(db_tx.user_id),
        "amount": db_tx.amount,
        "transaction_type": db_tx.transaction_type.value,
        "timestamp": db_tx.timestamp.isoformat(),
        "location": db_tx.location,
        "status": db_tx.status.value,
        "is_fraud": db_tx.is_fraud,
        "anomaly_score": db_tx.anomaly_score
    }
    await manager.broadcast_to_user(str(db_tx.user_id), tx_dict)

    return db_tx


@router.get(
    "/",
    response_model=List[TransactionResponse],
    summary="Get user transactions",
)
async def get_transactions(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Return recent transactions for the authenticated user.
    """
    transactions = db.query(Transaction)\
                     .filter(Transaction.user_id == current_user.id)\
                     .order_by(desc(Transaction.timestamp))\
                     .limit(limit)\
                     .all()
    return transactions


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time transaction streaming.
    Authentication is done via 'token' query parameter.
    """
    try:
        token_data = AuthService.decode_token(token)
        user = db.query(User).filter(User.username == token_data.username).first()
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id_str = str(user.id)
    await manager.connect(websocket, user_id_str)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id_str)
