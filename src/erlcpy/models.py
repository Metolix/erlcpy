from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any


@dataclass(slots=True)
class Model:
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: getattr(self, item.name)
            for item in fields(self)
            if item.name != "raw"
        }


@dataclass(slots=True)
class Location(Model):
    x: float | None = None
    z: float | None = None
    postal_code: str | None = None
    street_name: str | None = None
    building_number: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Location":
        return cls(
            x=data.get("LocationX"),
            z=data.get("LocationZ"),
            postal_code=data.get("PostalCode"),
            street_name=data.get("StreetName"),
            building_number=data.get("BuildingNumber"),
            raw=data,
        )


@dataclass(slots=True)
class Player(Model):
    username: str = ""
    roblox_id: int | None = None
    team: str = ""
    permission: str = ""
    callsign: str | None = None
    location: Location | None = None
    wanted_stars: int = 0

    @property
    def is_wanted(self) -> bool:
        return self.wanted_stars > 0

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Player":
        value = data.get("Player", "")
        username, separator, identifier = value.partition(":")
        try:
            roblox_id = int(identifier) if separator and identifier else None
        except ValueError:
            roblox_id = None
        location = data.get("Location")
        return cls(
            username=username or value,
            roblox_id=roblox_id,
            team=data.get("Team", ""),
            permission=data.get("Permission", ""),
            callsign=data.get("Callsign"),
            location=Location.from_api(location) if isinstance(location, dict) else None,
            wanted_stars=data.get("WantedStars", 0),
            raw=data,
        )


@dataclass(slots=True)
class Staff(Model):
    co_owner_ids: list[int] = field(default_factory=list)
    admins: dict[str, str] = field(default_factory=dict)
    mods: dict[str, str] = field(default_factory=dict)
    helpers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Staff":
        return cls(
            co_owner_ids=data.get("CoOwners", []),
            admins=data.get("Admins", {}),
            mods=data.get("Mods", {}),
            helpers=data.get("Helpers", {}),
            raw=data,
        )


@dataclass(slots=True)
class JoinLog(Model):
    joined: bool = False
    timestamp: int = 0
    player: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "JoinLog":
        return cls(
            joined=data.get("Join", False),
            timestamp=data.get("Timestamp", 0),
            player=data.get("Player", ""),
            raw=data,
        )


@dataclass(slots=True)
class KillLog(Model):
    killed: str = ""
    timestamp: int = 0
    killer: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "KillLog":
        return cls(
            killed=data.get("Killed", ""),
            timestamp=data.get("Timestamp", 0),
            killer=data.get("Killer", ""),
            raw=data,
        )


@dataclass(slots=True)
class CommandLog(Model):
    player: str = ""
    timestamp: int = 0
    command: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CommandLog":
        return cls(
            player=data.get("Player", ""),
            timestamp=data.get("Timestamp", 0),
            command=data.get("Command", ""),
            raw=data,
        )


@dataclass(slots=True)
class ModCall(Model):
    caller: str = ""
    moderator: str | None = None
    timestamp: int = 0

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "ModCall":
        return cls(
            caller=data.get("Caller", ""),
            moderator=data.get("Moderator"),
            timestamp=data.get("Timestamp", 0),
            raw=data,
        )


@dataclass(slots=True)
class EmergencyCall(Model):
    team: str = ""
    caller_id: int | None = None
    player_ids: list[int] = field(default_factory=list)
    position: tuple[float, float] | None = None
    started_at: int = 0
    call_number: int | None = None
    description: str = ""
    position_descriptor: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "EmergencyCall":
        position = data.get("Position")
        coordinates = (
            (float(position[0]), float(position[1]))
            if isinstance(position, list) and len(position) >= 2
            else None
        )
        return cls(
            team=data.get("Team", ""),
            caller_id=data.get("Caller"),
            player_ids=data.get("Players", []),
            position=coordinates,
            started_at=data.get("StartedAt", 0),
            call_number=data.get("CallNumber"),
            description=data.get("Description", ""),
            position_descriptor=data.get("PositionDescriptor", ""),
            raw=data,
        )


@dataclass(slots=True)
class Vehicle(Model):
    name: str = ""
    owner: str = ""
    plate: str | None = None
    texture: str | None = None
    color_hex: str | None = None
    color_name: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Vehicle":
        return cls(
            name=data.get("Name", ""),
            owner=data.get("Owner", ""),
            plate=data.get("Plate"),
            texture=data.get("Texture"),
            color_hex=data.get("ColorHex"),
            color_name=data.get("ColorName"),
            raw=data,
        )


@dataclass(slots=True)
class Server(Model):
    name: str = ""
    owner_id: int = 0
    co_owner_ids: list[int] = field(default_factory=list)
    current_players: int = 0
    max_players: int = 0
    join_key: str = ""
    account_verification_requirement: str = ""
    team_balance: bool = False
    players: list[Player] | None = None
    staff: Staff | None = None
    join_logs: list[JoinLog] | None = None
    queue: list[int] | None = None
    kill_logs: list[KillLog] | None = None
    command_logs: list[CommandLog] | None = None
    mod_calls: list[ModCall] | None = None
    emergency_calls: list[EmergencyCall] | None = None
    vehicles: list[Vehicle] | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Server":
        return cls(
            name=data.get("Name", ""),
            owner_id=data.get("OwnerId", 0),
            co_owner_ids=data.get("CoOwnerIds", []),
            current_players=data.get("CurrentPlayers", 0),
            max_players=data.get("MaxPlayers", 0),
            join_key=data.get("JoinKey", ""),
            account_verification_requirement=data.get("AccVerifiedReq", ""),
            team_balance=data.get("TeamBalance", False),
            players=[Player.from_api(item) for item in data["Players"]] if "Players" in data else None,
            staff=Staff.from_api(data["Staff"]) if "Staff" in data else None,
            join_logs=[JoinLog.from_api(item) for item in data["JoinLogs"]] if "JoinLogs" in data else None,
            queue=data.get("Queue"),
            kill_logs=[KillLog.from_api(item) for item in data["KillLogs"]] if "KillLogs" in data else None,
            command_logs=[CommandLog.from_api(item) for item in data["CommandLogs"]] if "CommandLogs" in data else None,
            mod_calls=[ModCall.from_api(item) for item in data["ModCalls"]] if "ModCalls" in data else None,
            emergency_calls=[EmergencyCall.from_api(item) for item in data["EmergencyCalls"]] if "EmergencyCalls" in data else None,
            vehicles=[Vehicle.from_api(item) for item in data["Vehicles"]] if "Vehicles" in data else None,
            raw=data,
        )


@dataclass(slots=True)
class CommandResult(Model):
    message: str = ""
    command_id: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CommandResult":
        return cls(
            message=data.get("message", ""),
            command_id=data.get("commandId"),
            raw=data,
        )
