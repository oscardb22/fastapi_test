from datetime import datetime

import factory

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import Users


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Users
        sqlalchemy_get_or_create = (
            "full_name",
            "cellphone",
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
    email = factory.Faker("email", locale=settings.LANGUAGE_CODE)
    full_name = factory.Faker("name", locale=settings.LANGUAGE_CODE)
    cellphone = factory.Faker("phone_number", locale=settings.LANGUAGE_CODE)
    hashed_password = factory.Faker("password", locale=settings.LANGUAGE_CODE)
    is_active = True
    date_joined = datetime.now()

    @factory.post_generation
    def user_set_password(self, create, extracted, **kwargs):
        if create:
            self.hashed_password = get_password_hash(self.hashed_password)
        if extracted:
            self.hashed_password = get_password_hash(extracted.hashed_password)
        UserFactory._meta.sqlalchemy_session.commit()
