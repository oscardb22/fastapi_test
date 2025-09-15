from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.cruds.users import create_user
from app.models.user import Users

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False}
)


def init_db(session: Session) -> None:
    user = session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = Users(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        create_user(session=session, user_create=user_in)
