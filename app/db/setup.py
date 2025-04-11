from sqlmodel import Session, SQLModel, create_engine

from app.config import env
from app.log.console import log_info

DB_URL = env.get_env("DB_URL", "sqlite:///./app.db")
engine = create_engine(DB_URL)


def connect_db():
    log_info("Connecting to database...")
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as session:
        yield session
