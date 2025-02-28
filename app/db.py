from sqlmodel import Session, create_engine
from settings import settings
from sqlalchemy.orm import sessionmaker

URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_IP}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
