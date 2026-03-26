from collections.abc import AsyncGenerator
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker

engine = create_engine(settings.database_url)

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)



class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[Session, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
