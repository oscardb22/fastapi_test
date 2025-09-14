from fastapi import APIRouter

from app.api.routes import general, jose_auth, open_ai, private, py_jwt_auth
from app.core.config import DEV_ENVIRONMENT, settings

api_router = APIRouter()
api_router.include_router(general.router)
api_router.include_router(jose_auth.router)
api_router.include_router(py_jwt_auth.router)
api_router.include_router(open_ai.router)


if settings.ENVIRONMENT == DEV_ENVIRONMENT:
    api_router.include_router(private.router)
