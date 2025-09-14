from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.cruds.users import create_user
from app.models.user import Users

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    user = session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = Users(
            email=settings.FIRST_SUPERUSER,
            hashed_password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        create_user(session=session, user_create=user_in)
