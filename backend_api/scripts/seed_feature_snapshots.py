from db.connection import SessionLocal
from models.feature_snapshot import FeatureSnapshot
from datetime import datetime
import random

def seed_feature_snapshots():
    db = SessionLocal()
    try:
        for i in range(5):
            snapshot = FeatureSnapshot(
                user_id="user_qa_001",
                ticker="AAPL",
                interval="15m",
                values=[round(random.uniform(-1, 1), 3) for _ in range(90)],
                created_at=datetime.utcnow()
            )
            db.add(snapshot)
        db.commit()
        print("✅ Seeded 5 feature snapshots.")
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_feature_snapshots()
