# API Reference

## Module `shelly_rpc`

### `ShellyClient(host, *, username=None, password=None, use_https=False, timeout=10.0)`

Client for the local Shelly RPC API.

Parameters:
- `host: str`
  - IP/hostname (`192.168.33.1`) or full URL (`http://192.168.33.1`).
- `username: str | None`
  - username for digest auth.
- `password: str | None`
  - password for digest auth.
- `use_https: bool`
  - use HTTPS when `host` is provided without a scheme.
- `timeout: float`
  - HTTP request timeout in seconds.

Host normalization behavior:
- `"192.168.1.10"` -> `http://192.168.1.10`
- `"https://example.local/"` -> `https://example.local`

### `call(method, params=None) -> RpcResult`

Runs a JSON-RPC call via `POST /rpc`.

Request shape:

```json
{
  "id": <auto increment>,
  "method": "<MethodName>",
  "params": { ... }
}
```

Return behavior:
- if `result` exists -> returns `result`;
- if `error` exists -> raises `ShellyRpcError`;
- otherwise returns the full JSON response object.

### `call_method_endpoint(method, params=None) -> RpcResult`

Runs a call via `POST /rpc/<method>`.

Payload behavior:
- request body contains only `params` (or `{}` when `None`).

Return behavior:
- returns JSON response;
- raises `ShellyRpcError` if `error` is present.

### Convenience methods

- `get_device_info()`
  - Equivalent to: `Shelly.GetDeviceInfo`.
- `get_status()`
  - Equivalent to: `Shelly.GetStatus`.
- `switch_get_status(switch_id=0)`
  - Equivalent to: `Switch.GetStatus`.
- `switch_set(switch_id, on)`
  - Equivalent to: `Switch.Set`.
- `switch_toggle(switch_id)`
  - Equivalent to: `Switch.Toggle`.

## Exceptions

### `ShellyError`
Base exception class for this library.

### `ShellyTransportError(ShellyError)`
Transport-level exception.

Typical cases:
- network/connectivity issues;
- HTTP status errors;
- invalid JSON response from device.

### `ShellyRpcError(ShellyError)`
Raised when the Shelly device returns an RPC `error` object.

Attributes:
- `code: int`
- `message: str`
- `data: object | None`

Handling example:

```python
from shelly_rpc import ShellyClient, ShellyRpcError

client = ShellyClient("192.168.33.1")

try:
    client.switch_get_status(7)
except ShellyRpcError as e:
    print(e.code, e.message)
```
