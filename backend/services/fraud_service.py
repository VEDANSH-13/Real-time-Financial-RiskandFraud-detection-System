"""
Fraud detection engine using Rule-based logic and Isolation Forest ML.
"""

from typing import List
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import IsolationForest
import numpy as np

class FraudDetectionService:
    def __init__(self):
        print("Initializing ML Fraud Detection Service...")
        # Train baseline IsolationForest for Amount anomaly detection
        # Realistic baseline transactions: $5 to $500 mostly, some $1000 bounds.
        np.random.seed(42)
        normal_data = np.random.normal(150, 100, 1000)
        # Add some slight heavy tails, clip to positive
        normal_data = np.clip(normal_data, 5, 2000)
        
        # IsolationForest expects 2D array
        self.X_train = normal_data.reshape(-1, 1)
        
        self.model = IsolationForest(
            n_estimators=100,
            max_samples='auto',
            contamination=0.05, # Expecting 5% anomalies
            random_state=42
        )
        # Fit baseline model
        self.model.fit(self.X_train)
        print("Isolation Forest trained successfully.")

    def evaluate_transaction(self, amount: float, recent_txs: List) -> tuple[bool, float]:
        """
        Evaluate single transaction against rules and ML model.
        Returns:
            (is_fraud: bool, anomaly_score: float)
        """
        is_fraud = False
        
        # 1. Evaluate ML Anomaly Score
        # score_samples returns negative scores for anomalies (lower is more anomalous). 
        # Range is generally [-0.5, 0] or so. We normalize mathematically.
        # Positive score -> Normal, Negative score -> Anomaly.
        ml_score_raw = self.model.score_samples(np.array([[amount]]))[0]
        
        # Map raw roughly [-0.5, 0.2] to [0.0, 1.0]. Lower raw -> closer to 1.0 (fraud).
        # We invert it so higher score = MORE anomalous.
        # E.g., if raw = -0.3, anomaly_score = 0.8
        anomaly_score = max(0.0, min(1.0, (-ml_score_raw / 0.5)))
        
        # 2. Rule-Based Engine
        # Rule 1: High Transaction Amount Override
        if amount > 10000:
            is_fraud = True
            anomaly_score = 1.0  # Max score

        # Rule 2: Velocity Check (e.g., >3 transactions in last 60 seconds)
        # recent_txs comes sorted descending by timestamp
        if len(recent_txs) >= 3:
            now = datetime.now(timezone.utc)
            # count how many happened in the last 60 seconds
            rapid_txs = [tx for tx in recent_txs if (now - tx.timestamp).total_seconds() < 60]
            if len(rapid_txs) >= 3:
                is_fraud = True
                anomaly_score = max(anomaly_score, 0.95)

        # ML Threshold override
        if anomaly_score > 0.8:
            is_fraud = True

        return is_fraud, round(anomaly_score, 4)

# Global singleton
fraud_engine = FraudDetectionService()
