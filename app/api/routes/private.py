from fastapi import APIRouter

from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/private", tags=["private"])


@router.get("/sentry-debug-dispatch-error")
async def trigger_error():
    """
    This endpoint is used to trigger a sentry error for testing purposes.
    """
    logger.info("Triggering sentry error")
    try:
        division_by_zero = 1 / 0
        return division_by_zero
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"status": "success", "message": "Error dispatched correctly"}
