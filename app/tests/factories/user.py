from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from models.user import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    name = Faker("name")
    email = Faker("email")
