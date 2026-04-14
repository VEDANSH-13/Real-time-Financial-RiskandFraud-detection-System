import os
import sys

# Ensure backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from config.database import engine

def migrate():
    print("Running DB Migration: Adding fraud columns...")
    with engine.connect() as conn:
        try:
            # Postgres safe add columns
            conn.execute(text("ALTER TABLE transactions Add COLUMN IF NOT EXISTS is_fraud BOOLEAN DEFAULT false;"))
            conn.execute(text("ALTER TABLE transactions Add COLUMN IF NOT EXISTS anomaly_score FLOAT DEFAULT 0.0;"))
            conn.commit()
            print("Successfully updated the transactions table schema!")
        except Exception as e:
            print(f"Error updating schema: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
