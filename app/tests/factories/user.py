from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from dependencies.database import session
from models.user import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = session

    name = Faker("name")
    email = Faker("email")
