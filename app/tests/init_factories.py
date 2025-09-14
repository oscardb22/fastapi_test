from sqlmodel import Session

from app.tests.test_factories.test_token import TokenFactory
from app.tests.test_factories.test_user import UserFactory


def init_factories(session: Session) -> None:
    UserFactory._meta.sqlalchemy_session = session
    TokenFactory._meta.sqlalchemy_session = session
