import sys
from os.path import abspath, dirname
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import Session, SQLModel, delete

sys.path.append(dirname(dirname(abspath(__file__))))

from factory.alchemy import SQLAlchemyModelFactory  # noqa: E402

from config import settings  # noqa: E402
from dependencies.database import get_session  # noqa: E402
from main import app  # noqa: E402
from models.todo import Todo  # noqa
from models.user import User  # noqa

engine = create_engine(
    URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="rootpassword",
        host=settings.db_host,
        database="task-track_test",  # テストDBを指定
    )
)


@pytest.fixture(scope="function")
def test_app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = app
    yield _app


@pytest.fixture(scope="session")
def db_engine():

    if not database_exists(engine.url):
        create_database(engine.url)

    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, Any, None]:
    from .factories.todo import TodoFactory  # noqa
    from .factories.user import UserFactory  # noqa

    with Session(engine) as session:
        # Ensure that all factories use the same session
        for factory in SQLAlchemyModelFactory.__subclasses__():
            factory._meta.sqlalchemy_session = session
        yield session

        # テスト後の処理: データベースのデータをクリア
        # 外部キーの制約エラーの為、手動で削除の順番を制御する
        for model_class in [Todo, User]:
            session.execute(delete(model_class))
        # for table in list(SQLModel.metadata.tables.values()):
        #     session.execute(table.delete())
        session.commit()


@pytest.fixture
def auth_headers():
    return {"Authorization": "expected_token"}  # noqa: E501


@pytest.fixture(scope="function")
def client(
    test_app: FastAPI, db_session: Session, auth_headers: dict
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    test_app.dependency_overrides[get_session] = _get_test_db
    with TestClient(test_app) as client:
        client.headers.update(auth_headers)
        yield client
