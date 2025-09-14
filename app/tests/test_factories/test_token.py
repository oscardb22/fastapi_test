import factory

from app.models.user import Tokens
from app.tests.test_factories.test_user import UserFactory


class TokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tokens
        sqlalchemy_get_or_create = (
            "token",
            "users",
        )
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    token = factory.Sequence(lambda n: f"user{n}")
    users = factory.SubFactory(UserFactory)
