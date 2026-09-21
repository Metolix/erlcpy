from prcpy.models import Player, Server, Staff


def test_player_parsing() -> None:
    player = Player.from_api(
        {
            "Player": "Sidhak:123",
            "Team": "Police",
            "Permission": "Normal",
            "WantedStars": 2,
            "Location": {
                "LocationX": 10.5,
                "LocationZ": 20.5,
                "PostalCode": "218",
            },
        }
    )
    assert player.username == "Sidhak"
    assert player.roblox_id == 123
    assert player.is_wanted
    assert player.location is not None
    assert player.location.x == 10.5


def test_staff_helpers_are_parsed() -> None:
    staff = Staff.from_api(
        {
            "CoOwners": [1],
            "Admins": {"2": "Admin"},
            "Helpers": {"3": "Helper"},
        }
    )
    assert staff.co_owner_ids == [1]
    assert staff.admins["2"] == "Admin"
    assert staff.helpers["3"] == "Helper"


def test_server_parsing() -> None:
    server = Server.from_api(
        {
            "Name": "Test",
            "OwnerId": 1,
            "CoOwnerIds": [2],
            "CurrentPlayers": 1,
            "MaxPlayers": 40,
            "JoinKey": "TEST",
            "AccVerifiedReq": "Disabled",
            "TeamBalance": True,
            "Players": [{"Player": "A:3", "Team": "Civilian"}],
        }
    )
    assert server.name == "Test"
    assert server.players is not None
    assert server.players[0].username == "A"
