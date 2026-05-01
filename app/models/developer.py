from sqlalchemy import Column, Integer, String
from .base import Base

class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)