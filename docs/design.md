# Design notes

prcpy keeps the public API small.

## Typed models

Documented response objects are converted into Python dataclasses. The original API response is retained in each model's `raw` attribute so applications do not lose fields when the API adds information.

## v1 and v2

The package uses v2 for the consolidated server endpoint and command execution. The individual v1 endpoints remain available as convenience methods because they are documented API endpoints and can be useful when an application only needs one resource.

## Rate limits

Every response updates `Client.rate_limit`. The library does not automatically retry requests. Automatic retries are especially risky for POST commands because an application cannot always determine whether the server executed a command before a connection failure.

## Low-level access

`request()` exists so users do not have to wait for a package release whenever the API exposes a new endpoint.

## Dependencies

The runtime dependency is only httpx. Webhook verification is optional and isolated behind the `webhooks` extra.
