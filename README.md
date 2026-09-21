# erlcpy

A typed Python client for the ER:LC Private Server API.

erlcpy provides synchronous and asynchronous clients, typed response models, rate-limit metadata, structured exceptions, webhook helpers, and a low-level request interface for endpoints that are added to the API later.

> erlcpy is an independent open-source project and is not affiliated with or endorsed by ER:LC or PRC.

## Requirements

- Python 3.10+
- An ER:LC private server with API access
- A server key from the server's API settings

## Installation

```bash
pip install erlcpy
```

For webhook signature verification:

```bash
pip install "erlcpy[webhooks]"
```

## Quick start

```python
from erlcpy import Client

with Client("your-server-key") as client:
    server = client.get_server(players=True)

    print(server.name)
    print(f"{server.current_players}/{server.max_players}")

    for player in server.players or []:
        print(player.username, player.team)
```

## Async

```python
from erlcpy import AsyncClient

async with AsyncClient("your-server-key") as client:
    server = await client.get_server(players=True)
    print(server.name)
```

## Available server data

The v2 server endpoint supports these optional resources:

- `players`
- `staff`
- `join_logs`
- `queue`
- `kill_logs`
- `command_logs`
- `mod_calls`
- `emergency_calls`
- `vehicles`

Only request the data an application needs.

```python
server = client.get_server(
    players=True,
    staff=True,
    vehicles=True,
    emergency_calls=True,
)
```

## Convenience methods

```python
players = client.get_players()
staff = client.get_staff()
join_logs = client.get_join_logs()
queue = client.get_queue()
kill_logs = client.get_kill_logs()
command_logs = client.get_command_logs()
mod_calls = client.get_mod_calls()
emergency_calls = client.get_emergency_calls()
vehicles = client.get_vehicles()
bans = client.get_bans()
```

## Commands

```python
result = client.send_command(":h Hello from erlcpy")
print(result.message)
```

The API documents a `commandId` on command failures. erlcpy exposes it as `CommandError.command_id` or `ServerOfflineError.command_id` when supplied by the API.

## Authentication

All API requests use the `server-key` header.

Public applications may also provide a global API key:

```python
client = Client(
    "server-key",
    global_api_key="global-api-key",
)
```

Environment variables are supported:

```text
ERLC_SERVER_KEY=...
ERLC_GLOBAL_API_KEY=...
```

```python
client = Client.from_env()
```

Never commit keys to source control.

## Rate limits

The client reads the API's `X-RateLimit-Bucket`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` response headers.

```python
response = client.get_server()
print(client.rate_limit)
```

A 429 response raises `RateLimitError` with `retry_after` when the server provides a `Retry-After` header.

erlcpy does not silently retry commands. This avoids accidentally executing an in-game command more than once.

## Raw API access

The typed methods cover the documented API, but the API can grow independently of this package.

```python
data = client.request("GET", "/v2/server", params={"Players": "true"})
```

Set `parse=False` on typed methods when the raw response is required.

## Webhooks

erlcpy includes a small helper for Ed25519 webhook verification:

```python
from erlcpy.webhooks import verify_signature

verify_signature(
    timestamp=request.headers["X-Signature-Timestamp"],
    signature=request.headers["X-Signature-Ed25519"],
    body=raw_request_body,
    public_key="your-webhook-public-key",
)
```

Always verify the raw request body before parsing JSON.

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
```

## Project structure

```text
erlcpy/
├── docs/
├── examples/
├── src/erlcpy/
│   ├── client.py
│   ├── errors.py
│   ├── models.py
│   ├── rate_limits.py
│   └── webhooks.py
├── tests/
├── .github/workflows/
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## License

MIT
