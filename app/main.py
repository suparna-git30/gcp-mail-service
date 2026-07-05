from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.config.settings import get_settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.logger import get_logger
from fastapi.responses import JSONResponse
from fastapi import Request

from app.exceptions.custom_exceptions import MailAutomationException


settings = get_settings()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Application started",
        extra={
            "environment": settings.environment,
            "version": settings.app_version,
            "application": settings.app_name,
        },
    )

    yield

    logger.info("Application stopped")

app = FastAPI(
    title=settings.app_name,
    description="Enterprise Mail Automation Service",
    version=settings.app_version,
    lifespan=lifespan
    )

# Add middleware AFTER creating the app
app.add_middleware(LoggingMiddleware)

# -------------------------
# Exception Handler
# -------------------------
@app.exception_handler(MailAutomationException)
async def custom_exception_handler(
    request: Request,
    exc: MailAutomationException,
):
    logger.error(
        "MailAutomationException occurred",
        extra={
            "path": request.url.path,
            "error": exc.message,
        },
    )

    return JSONResponse(
        status_code=400,
        content={
            "error": exc.message,
        },
    )


# -------------------------
# Routes
# -------------------------


@app.get("/")
def home():
    logger.info("Home endpoint called",extra={
        "environment": settings.environment,
        "version": settings.app_version,
        "application": settings.app_name,
    },)
    return {"message": "Welcome to Mail Automation API"}


@app.get("/health")
def health():
    return {
        "status": "UP"
    }

@app.get("/config")
def config():

    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/error")
def test_error():

    raise MailAutomationException(
        "Sample enterprise exception"
    )