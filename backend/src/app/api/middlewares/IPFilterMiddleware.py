from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from app.core import config
from app.exceptions.api import ApiError


class IPFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.client.host != config.PROXY_HOST:
            raise ApiError.forbidden(message="Access denied")
        response = await call_next(request)
        return response
