import logging

from fastapi import FastAPI

from app.core.config import settings
from app.routes.health import router as health_router

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application starting...")


@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }