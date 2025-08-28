from datetime import datetime

import factory

from apps.authentication.models.user import Users
from settings import LANGUAGE_CODE, bcrypt_context


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Users
        sqlalchemy_get_or_create = (
            "username",
            "email",
            "hashed_password",
            "is_active",
            "date_joined"
        )
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    # id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Faker("email", locale=LANGUAGE_CODE)
    hashed_password = factory.Faker("password", locale=LANGUAGE_CODE)
    is_active = True
    date_joined = datetime.now()

    @factory.post_generation
    def user_set_password(self, create, extracted, **kwargs):
        if create:
            self.hashed_password = bcrypt_context.hash(self.hashed_password)
        if extracted:
            self.hashed_password = bcrypt_context.hash(extracted.hashed_password)
        UserFactory._meta.sqlalchemy_session.commit()
