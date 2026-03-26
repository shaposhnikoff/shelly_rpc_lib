# Changelog

All notable changes to this project are documented in this file.

## [0.1.0] - 2026-03-26

### Added
- Initial `shelly_rpc` Python client for local Shelly RPC API (Gen2/Gen3/Gen4).
- HTTP JSON-RPC client with `call()` and `call_method_endpoint()` support.
- Convenience methods for:
  - `Shelly.GetDeviceInfo`
  - `Shelly.GetStatus`
  - `Switch.GetStatus`
  - `Switch.Set`
  - `Switch.Toggle`
- Digest authentication support (urllib `HTTPDigestAuthHandler`).
- Error model:
  - `ShellyTransportError`
  - `ShellyRpcError` with `code`, `message`, `data`.
- Documentation in English:
  - main README
  - API reference
  - usage examples including device-specific sections for
    - Shelly 1PM Mini Gen3
    - Shelly Plus 1
    - Shelly Pro 3EM
- Unit tests for client behavior and error handling.
