from app.storage.db import SessionLocal
from sqlalchemy import text

def test_connection():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT 1"))
        print("DB connected successfully")
        print("Result:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)
    finally:
        session.close()

if __name__ == "__main__":
    test_connection()