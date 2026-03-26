# shelly-rpc

A Python library for the local Shelly RPC API (Gen2/Gen3/Gen4).

The library provides:
- a single HTTP JSON-RPC client for `http://<device>/rpc`;
- digest authentication support;
- convenience methods for common operations (`Shelly.GetStatus`, `Switch.Set`);
- a unified transport and RPC error layer.

## Contents

- Quick Start
- Authentication
- Supported Methods
- Error Handling
- API Documentation
- Usage Examples
- Build and Release
- Development and Tests

## Quick Start

### 1) Install

```bash
cd /mnt/NetworkBackupShare/api_doc/shelly_rpc
python3 -m pip install -e .
```

### 2) Basic usage

```python
from shelly_rpc import ShellyClient, ShellyRpcError, ShellyTransportError

client = ShellyClient("192.168.33.1")

try:
    info = client.get_device_info()
    status = client.get_status()

    relay0_before = client.switch_get_status(0)
    client.switch_set(0, True)
    relay0_after = client.switch_get_status(0)

    print("model:", info.get("model"))
    print("before:", relay0_before.get("output"))
    print("after:", relay0_after.get("output"))
except ShellyRpcError as e:
    print(f"RPC error: code={e.code} message={e.message}")
except ShellyTransportError as e:
    print(f"Transport error: {e}")
```

## Authentication

If digest authentication is enabled on the device:

```python
from shelly_rpc import ShellyClient

client = ShellyClient(
    "192.168.33.1",
    username="admin",
    password="secret",
)
```

For HTTPS, pass `use_https=True`.

## Supported Methods (v1)

### Generic methods
- `call(method, params=None)`
- `call_method_endpoint(method, params=None)`

### Convenience methods
- `get_device_info()` -> `Shelly.GetDeviceInfo`
- `get_status()` -> `Shelly.GetStatus`
- `switch_get_status(switch_id=0)` -> `Switch.GetStatus`
- `switch_set(switch_id, on)` -> `Switch.Set`
- `switch_toggle(switch_id)` -> `Switch.Toggle`

## Error Handling

- `ShellyTransportError`
  - network errors;
  - HTTP errors;
  - invalid JSON responses.
- `ShellyRpcError`
  - RPC errors returned by the device in the `error` field;
  - includes `code`, `message`, and `data`.

Example Shelly API error codes (from local docs):
- `-103` -> invalid argument (for example, missing required `id`)
- `-105` -> not found (for example, `Bad id=7`)

## API Documentation

- Detailed class and method reference: [docs/API.md](docs/API.md)
- Ready-to-run usage scenarios: [docs/EXAMPLES.md](docs/EXAMPLES.md)
- Build and release instructions (uv): [docs/BUILD.md](docs/BUILD.md)

## Development and Tests

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Sources (local docs snapshot)

- `shelly-api-docs.shelly.cloud/gen2/General/RPCChannels/index.html`
- `shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly/index.html`
- `shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch/index.html`
- `shelly-api-docs.shelly.cloud/gen2/General/CommonErrors/index.html`
