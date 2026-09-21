import httpx
import respx
import pytest

from erlcpy import AuthenticationError, Client, RateLimitError


@respx.mock
def test_server_request() -> None:
    route = respx.get("https://api.erlc.gg/v2/server").mock(
        return_value=httpx.Response(
            200,
            json={
                "Name": "Test",
                "OwnerId": 1,
                "CoOwnerIds": [],
                "CurrentPlayers": 1,
                "MaxPlayers": 40,
                "JoinKey": "TEST",
                "AccVerifiedReq": "Disabled",
                "TeamBalance": True,
            },
        )
    )
    with Client("secret") as client:
        server = client.get_server()
    assert route.called
    assert server.name == "Test"


@respx.mock
def test_authentication_error() -> None:
    respx.get("https://api.erlc.gg/v2/server").mock(
        return_value=httpx.Response(403, json={"message": "Unauthorized"})
    )
    with Client("secret") as client:
        with pytest.raises(AuthenticationError) as error:
            client.get_server()
    assert error.value.status_code == 403


@respx.mock
def test_rate_limit_metadata() -> None:
    respx.get("https://api.erlc.gg/v2/server").mock(
        return_value=httpx.Response(
            200,
            headers={
                "X-RateLimit-Bucket": "global",
                "X-RateLimit-Limit": "35",
                "X-RateLimit-Remaining": "34",
                "X-RateLimit-Reset": "1704614400",
            },
            json={"Name": "Test"},
        )
    )
    with Client("secret") as client:
        client.get_server()
        assert client.rate_limit is not None
        assert client.rate_limit.bucket == "global"
        assert client.rate_limit.remaining == 34


@respx.mock
def test_rate_limit_error() -> None:
    respx.get("https://api.erlc.gg/v2/server").mock(
        return_value=httpx.Response(
            429,
            headers={"Retry-After": "2"},
            json={"message": "Too many requests"},
        )
    )
    with Client("secret") as client:
        with pytest.raises(RateLimitError) as error:
            client.get_server()
    assert error.value.retry_after == 2
