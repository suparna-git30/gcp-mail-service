from time import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time()

        logger.info(f"Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        duration = time() - start

        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"Status={response.status_code} "
            f"Duration={duration:.3f}s"
        )

        return response