from __future__ import annotations

from typing import Any


class ERLCError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_code: int | str | None = None,
        details: Any = None,
        command_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        self.command_id = command_id

    def __str__(self) -> str:
        return self.message


class APIError(ERLCError):
    pass


class AuthenticationError(APIError):
    pass


class BadRequestError(APIError):
    pass


class RateLimitError(APIError):
    def __init__(
        self,
        message: str,
        *,
        retry_after: float | None = None,
        bucket: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
        self.bucket = bucket


class ServerOfflineError(APIError):
    pass


class CommandError(APIError):
    pass
