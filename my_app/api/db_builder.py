from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_db_session_factory(database_url: str) -> sessionmaker:
    engine = create_engine(database_url)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
