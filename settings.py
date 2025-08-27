from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
TOKEN_TYPE = config("TOKEN_TYPE")
SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")
OPENAI_API_KEY = config("OPENAI_API_KEY")
URL_CHAT_OPEN_AI = config("URL_CHAT_OPEN_AI")
REDIS_URL = config("REDIS_URL")
HEADER_OPEN_AI = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_bearer = OAuth2PasswordBearer(tokenUrl="token")
