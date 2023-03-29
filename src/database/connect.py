from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import settings

engine = create_engine(settings.db_url)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db
    except:
        db.close()
