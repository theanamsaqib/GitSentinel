from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base

class FileChange(Base):
    __tablename__ = "file_changes"

    id = Column(Integer, primary_key=True)
    commit_hash = Column(String, ForeignKey("commits.hash"))
    file_id = Column(Integer, ForeignKey("files.id"))
    lines_added = Column(Integer)
    lines_deleted = Column(Integer)