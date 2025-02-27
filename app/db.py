from sqlmodel import SQLModel, create_engine, Session
from settings import settings
from sqlalchemy.orm import sessionmaker

URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_IP}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(URL)

def get_session():
    session = sessionmaker(bind=engine, class_=Session)
    return session()

def init_db():
    SQLModel.metadata.create_all(engine)
