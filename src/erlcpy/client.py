from __future__ import annotations

import os
from typing import Any

import httpx

from .errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    CommandError,
    RateLimitError,
    ServerOfflineError,
)
from .models import (
    CommandLog,
    CommandResult,
    JoinLog,
    KillLog,
    ModCall,
    Player,
    Server,
    Staff,
    Vehicle,
)
from .rate_limits import RateLimitInfo

BASE_URL = "https://api.erlc.gg"

_INCLUDE_MAP = {
    "players": "Players",
    "staff": "Staff",
    "join_logs": "JoinLogs",
    "queue": "Queue",
    "kill_logs": "KillLogs",
    "command_logs": "CommandLogs",
    "mod_calls": "ModCalls",
    "emergency_calls": "EmergencyCalls",
    "vehicles": "Vehicles",
}


class _ClientBase:
    def __init__(
        self,
        server_key: str,
        *,
        global_api_key: str | None = None,
        base_url: str = BASE_URL,
        timeout: float | httpx.Timeout = 30.0,
    ) -> None:
        if not server_key.strip():
            raise ValueError("server_key must not be empty")
        self.server_key = server_key
        self.global_api_key = global_api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.rate_limit: RateLimitInfo | None = None

    @classmethod
    def from_env(cls, **kwargs: Any):
        server_key = os.getenv("ERLC_SERVER_KEY")
        if not server_key:
            raise ValueError("ERLC_SERVER_KEY is not set")
        return cls(
            server_key,
            global_api_key=os.getenv("ERLC_GLOBAL_API_KEY"),
            **kwargs,
        )

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "server-key": self.server_key,
            "User-Agent": "erlcpy/0.1.0",
        }
        if self.global_api_key:
            headers["Authorization"] = self.global_api_key
        return headers

    @staticmethod
    def _include_params(flags: dict[str, bool]) -> dict[str, str]:
        unknown = set(flags) - set(_INCLUDE_MAP)
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"Unknown server include(s): {names}")
        return {
            _INCLUDE_MAP[name]: "true"
            for name, enabled in flags.items()
            if enabled
        }

    def _raise_for_error(self, response: httpx.Response) -> None:
        if response.is_success:
            return
        try:
            payload = response.json()
        except ValueError:
            payload = None

        if isinstance(payload, dict):
            message = payload.get("message") or payload.get("error") or response.text
            error_code = payload.get("code")
            command_id = payload.get("commandId")
        else:
            message = response.text or response.reason_phrase
            error_code = None
            command_id = None

        common = {
            "status_code": response.status_code,
            "error_code": error_code,
            "details": payload,
            "command_id": command_id,
        }

        if response.status_code == 403:
            raise AuthenticationError(message, **common)
        if response.status_code == 400:
            raise BadRequestError(message, **common)
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            try:
                retry_after_value = float(retry_after) if retry_after else None
            except ValueError:
                retry_after_value = None
            raise RateLimitError(
                message,
                retry_after=retry_after_value,
                bucket=self.rate_limit.bucket if self.rate_limit else None,
                **common,
            )
        if response.status_code == 422:
            raise ServerOfflineError(message, **common)
        if response.request.method == "POST" and response.request.url.path.endswith("/command"):
            raise CommandError(message, **common)
        raise APIError(message, **common)

    @staticmethod
    def _json(response: httpx.Response) -> Any:
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise APIError(
                "The API returned an invalid JSON response.",
                status_code=response.status_code,
                details=response.text,
            ) from exc


class Client(_ClientBase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._http = httpx.Client(timeout=self.timeout)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self._http.request(
            method,
            f"{self.base_url}{path}" if path.startswith("/") else path,
            headers=self._headers(),
            **kwargs,
        )
        self.rate_limit = RateLimitInfo.from_headers(response.headers)
        self._raise_for_error(response)
        return self._json(response)

    def get_server(
        self,
        *,
        players: bool = False,
        staff: bool = False,
        join_logs: bool = False,
        queue: bool = False,
        kill_logs: bool = False,
        command_logs: bool = False,
        mod_calls: bool = False,
        emergency_calls: bool = False,
        vehicles: bool = False,
    ) -> Server:
        flags = {
            "players": players,
            "staff": staff,
            "join_logs": join_logs,
            "queue": queue,
            "kill_logs": kill_logs,
            "command_logs": command_logs,
            "mod_calls": mod_calls,
            "emergency_calls": emergency_calls,
            "vehicles": vehicles,
        }
        return Server.from_api(self.request("GET", "/v2/server", params=self._include_params(flags)))

    def get_players(self) -> list[Player]:
        return [Player.from_api(item) for item in self.request("GET", "/v1/server/players")]

    def get_staff(self) -> Staff:
        return Staff.from_api(self.request("GET", "/v1/server/staff"))

    def get_join_logs(self) -> list[JoinLog]:
        return [JoinLog.from_api(item) for item in self.request("GET", "/v1/server/joinlogs")]

    def get_queue(self) -> list[int]:
        return self.request("GET", "/v1/server/queue")

    def get_kill_logs(self) -> list[KillLog]:
        return [KillLog.from_api(item) for item in self.request("GET", "/v1/server/killlogs")]

    def get_command_logs(self) -> list[CommandLog]:
        return [CommandLog.from_api(item) for item in self.request("GET", "/v1/server/commandlogs")]

    def get_mod_calls(self) -> list[ModCall]:
        return [ModCall.from_api(item) for item in self.request("GET", "/v1/server/modcalls")]

    def get_bans(self) -> dict[str, Any]:
        return self.request("GET", "/v1/server/bans")

    def get_vehicles(self) -> list[Vehicle]:
        return [Vehicle.from_api(item) for item in self.request("GET", "/v1/server/vehicles")]

    def send_command(self, command: str) -> CommandResult:
        if not command.strip():
            raise ValueError("command must not be empty")
        return CommandResult.from_api(
            self.request("POST", "/v2/server/command", json={"command": command})
        )


class AsyncClient(_ClientBase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._http = httpx.AsyncClient(timeout=self.timeout)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = await self._http.request(
            method,
            f"{self.base_url}{path}" if path.startswith("/") else path,
            headers=self._headers(),
            **kwargs,
        )
        self.rate_limit = RateLimitInfo.from_headers(response.headers)
        self._raise_for_error(response)
        return self._json(response)

    async def get_server(
        self,
        *,
        players: bool = False,
        staff: bool = False,
        join_logs: bool = False,
        queue: bool = False,
        kill_logs: bool = False,
        command_logs: bool = False,
        mod_calls: bool = False,
        emergency_calls: bool = False,
        vehicles: bool = False,
    ) -> Server:
        flags = {
            "players": players,
            "staff": staff,
            "join_logs": join_logs,
            "queue": queue,
            "kill_logs": kill_logs,
            "command_logs": command_logs,
            "mod_calls": mod_calls,
            "emergency_calls": emergency_calls,
            "vehicles": vehicles,
        }
        data = await self.request("GET", "/v2/server", params=self._include_params(flags))
        return Server.from_api(data)

    async def get_players(self) -> list[Player]:
        data = await self.request("GET", "/v1/server/players")
        return [Player.from_api(item) for item in data]

    async def get_staff(self) -> Staff:
        return Staff.from_api(await self.request("GET", "/v1/server/staff"))

    async def get_join_logs(self) -> list[JoinLog]:
        data = await self.request("GET", "/v1/server/joinlogs")
        return [JoinLog.from_api(item) for item in data]

    async def get_queue(self) -> list[int]:
        return await self.request("GET", "/v1/server/queue")

    async def get_kill_logs(self) -> list[KillLog]:
        data = await self.request("GET", "/v1/server/killlogs")
        return [KillLog.from_api(item) for item in data]

    async def get_command_logs(self) -> list[CommandLog]:
        data = await self.request("GET", "/v1/server/commandlogs")
        return [CommandLog.from_api(item) for item in data]

    async def get_mod_calls(self) -> list[ModCall]:
        data = await self.request("GET", "/v1/server/modcalls")
        return [ModCall.from_api(item) for item in data]

    async def get_bans(self) -> dict[str, Any]:
        return await self.request("GET", "/v1/server/bans")

    async def get_vehicles(self) -> list[Vehicle]:
        data = await self.request("GET", "/v1/server/vehicles")
        return [Vehicle.from_api(item) for item in data]

    async def send_command(self, command: str) -> CommandResult:
        if not command.strip():
            raise ValueError("command must not be empty")
        data = await self.request("POST", "/v2/server/command", json={"command": command})
        return CommandResult.from_api(data)
