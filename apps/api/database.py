from collections.abc import AsyncGenerator
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker


def _create_engine():
    try:
        return create_engine(settings.database_url)
    except ImportError as exc:
        if "libodbc.so.2" in str(exc):
            raise RuntimeError(
                "No se pudo cargar unixODBC (falta libodbc.so.2). "
                "En Ubuntu instala al menos 'unixodbc' y 'unixodbc-dev'. "
                "Si tu DATABASE_URL usa 'driver=ODBC Driver 17 for SQL Server' "
                "o 'ODBC Driver 18 for SQL Server', instala tambien el driver "
                "de Microsoft correspondiente antes de iniciar la API o correr Alembic."
            ) from exc
        raise


engine = _create_engine()

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)



class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[Session, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
