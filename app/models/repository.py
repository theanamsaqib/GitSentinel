from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)