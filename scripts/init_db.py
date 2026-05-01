from app.storage.db import engine
from app.models.base import Base

from app.models.repository import Repository
from app.models.developer import Developer
from app.models.commit import Commit
from app.models.file import File
from app.models.file_changes import FileChange

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created")

if __name__ == "__main__":
    init_db()