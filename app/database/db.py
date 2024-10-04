import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
import app.database.settings as settings


class Base(DeclarativeBase): ...

engine = sa.create_engine(settings.DATABASE_URL)
