# API reference

## Client

### `Client(server_key, *, global_api_key=None, base_url=..., timeout=30)`

Synchronous API client.

### `Client.get_server(...)`

Fetches the v2 server endpoint. Optional boolean arguments map directly to the documented query parameters.

### `Client.get_players()`

Returns `list[Player]`.

### `Client.get_staff()`

Returns `Staff`.

### `Client.get_join_logs()`

Returns `list[JoinLog]`.

### `Client.get_queue()`

Returns Roblox user IDs waiting in the queue.

### `Client.get_kill_logs()`

Returns `list[KillLog]`.

### `Client.get_command_logs()`

Returns `list[CommandLog]`.

### `Client.get_mod_calls()`

Returns `list[ModCall]`.

### `Client.get_bans()`

Returns the raw bans object because the public API schema does not expose a richer stable structure.

### `Client.get_vehicles()`

Returns `list[Vehicle]`.

### `Client.send_command(command)`

Executes a command through the v2 command endpoint.

### `Client.request(method, path, **kwargs)`

Low-level access to the API. Authentication and error handling are still applied.

The asynchronous client exposes the same API with awaitable methods.
