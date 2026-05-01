from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .base import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"))
    file_path = Column(String)

    __table_args__ = (
        UniqueConstraint("repo_id", "file_path", name="unique_file_per_repo"),
    )