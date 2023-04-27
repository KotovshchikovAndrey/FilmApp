from __future__ import annotations

import typing as tp


class ApiError(Exception):
    status: int
    message: str
    details: tp.List[str]

    def __init__(self, status: int, message: str, details: tp.List[str]) -> None:
        self.status = status
        self.message = message
        self.details = details

    @classmethod
    def bad_request(cls, message: str, details: tp.List[str] = []) -> ApiError:
        return cls(status=400, message=message, details=details)

    @classmethod
    def unauthorized(cls, message: str, details: tp.List[str] = []) -> ApiError:
        return cls(status=401, message=message, details=details)

    @classmethod
    def forbidden(cls, message: str, details: tp.List[str] = []) -> ApiError:
        return cls(status=403, message=message, details=details)

    @classmethod
    def not_found(cls, message: str, details: tp.List[str] = []) -> ApiError:
        return cls(status=404, message=message, details=details)

    @classmethod
    def internal(cls, message: str, details: tp.List[str] = []) -> ApiError:
        return cls(status=500, message=message, details=details)
