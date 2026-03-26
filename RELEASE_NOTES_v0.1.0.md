# Release Notes - v0.1.0

Release date: 2026-03-26

## Highlights
- First public version of `shelly_rpc`.
- Local RPC support for Shelly Gen2/Gen3/Gen4 devices.
- Focused on reliable baseline operations and clear errors.

## Included in this release
- Generic RPC calls:
  - `call(method, params=None)`
  - `call_method_endpoint(method, params=None)`
- Convenience helpers:
  - `get_device_info()`
  - `get_status()`
  - `switch_get_status(switch_id=0)`
  - `switch_set(switch_id, on)`
  - `switch_toggle(switch_id)`
- Digest auth support.
- Unit tests.
- English documentation:
  - README
  - API reference
  - practical examples, including Plus 1, 1PM Mini Gen3, Pro 3EM.

## Notes
- This release is intentionally minimal and stable.
- Planned next iterations include broader component coverage and CI packaging pipeline.
