from app.storage.db import SessionLocal
from app.storage.repositories import get_or_create_repository
from app.storage.developers import get_or_create_developer

def test_insert():
    session = SessionLocal()

    repo = get_or_create_repository(
        session,
        name="gson",
        url="https://github.com/google/gson"
    )

    dev = get_or_create_developer(
        session,
        name="Test Dev",
        email="test@example.com"
    )

    print("Repository ID:", repo.id)
    print("Developer ID:", dev.id)

    session.close()

if __name__ == "__main__":
    test_insert()