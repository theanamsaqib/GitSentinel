from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from .base import Base

class Commit(Base):
    __tablename__ = "commits"

    hash = Column(String, primary_key=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"))
    author_id = Column(Integer, ForeignKey("developers.id"))
    commit_date = Column(DateTime)
    message = Column(String)