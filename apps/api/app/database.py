from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(settings.database_url)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)



class Base(DeclarativeBase):
    pass
