from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RateLimitInfo:
    bucket: str | None = None
    limit: int | None = None
    remaining: int | None = None
    reset: int | None = None

    @classmethod
    def from_headers(cls, headers: object) -> "RateLimitInfo":
        get = getattr(headers, "get")

        def integer(name: str) -> int | None:
            value = get(name)
            if value is None:
                return None
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        return cls(
            bucket=get("X-RateLimit-Bucket"),
            limit=integer("X-RateLimit-Limit"),
            remaining=integer("X-RateLimit-Remaining"),
            reset=integer("X-RateLimit-Reset"),
        )
