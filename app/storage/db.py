from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:%40anam1703@localhost:5432/gitsentinel"

engine = create_engine(
    DATABASE_URL,
    echo=True,          
    pool_pre_ping=True  
)

SessionLocal = sessionmaker(bind=engine)