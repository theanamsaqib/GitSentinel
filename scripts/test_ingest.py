from app.storage.db import SessionLocal
from app.processor.ingest import ingest_commit

def test_ingest():
    session = SessionLocal()

    fake_commit = {
        "hash": "abc123",
        "author_name": "Test Dev",
        "author_email": "test@example.com",
        "date": "2024-01-01",
        "message": "test commit",
        "files": [
            {"filename": "app.py", "added": 10, "deleted": 2}
        ]
    }

    ingest_commit(session, "https://github.com/test/repo", fake_commit)

    print("Ingestion complete")

    session.close()

if __name__ == "__main__":
    test_ingest()