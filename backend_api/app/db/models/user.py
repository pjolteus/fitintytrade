from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # e.g. Clerk/Firebase ID
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # optional: user, admin, analyst, etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Backref to predictions
    predictions = relationship("Prediction", back_populates="user")

    def __repr__(self):
        return f"<User {self.id} | {self.email}>"
