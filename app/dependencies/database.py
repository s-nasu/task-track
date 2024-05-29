from sqlmodel import Session, create_engine

from config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)

session = Session(engine)


def get_session():
    with Session(engine) as session:
        yield session
