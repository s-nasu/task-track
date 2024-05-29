from factory import Faker, Iterator, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker as OriginalFaker

from dependencies.database import session
from models.todo import TaskStatus, Todo

from .user import UserFactory

# 日本語のFakerインスタンスを作成
faker_jp = OriginalFaker("ja_JP")


class TodoFactory(SQLAlchemyModelFactory):
    """
    TodoFactoryはTodoモデルのためのファクトリクラスです。
    """

    class Meta:
        model = Todo
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = session

    title = Faker("pystr", max_chars=40, locale="ja_JP")
    """
    タイトルは最大40文字のランダムな文字列です。
    """

    description = Faker("paragraph", nb_sentences=3, locale="ja_JP")
    """
    説明は3つの文からなるランダムな段落です。
    """

    status = Iterator(TaskStatus)
    """
    ステータスはTaskStatusのイテレータです。
    """
    assignee = SubFactory(UserFactory)

    creator = SubFactory(UserFactory)

    updater = SubFactory(UserFactory)
