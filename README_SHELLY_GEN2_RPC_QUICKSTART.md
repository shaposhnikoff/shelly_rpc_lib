# Shelly Gen2/Plus/Pro Local RPC Quickstart (Status + Relay Control)

This quickstart is based on the local docs snapshot in this directory.
Target: local device API (`gen2`) for basic status checks and relay control.

## 1) RPC endpoint and transport

- Main HTTP RPC endpoint: `http://<SHELLY_IP_OR_HOST>/rpc`
- Method endpoint form is also supported: `http://<SHELLY_IP_OR_HOST>/rpc/<MethodName>`
- Example shown in docs: `Switch.Set` via query params: `/rpc/Switch.Set?id=0&on=true`

If digest auth is enabled on the device, use `curl --digest -u <user>:<password>`.

## 2) Setup

```bash
export SHELLY="192.168.33.1"
```

Optional (if auth enabled):

```bash
export SHELLY_USER="admin"
export SHELLY_PASS="your_password"
AUTH=(--digest -u "${SHELLY_USER}:${SHELLY_PASS}")
```

If auth is not enabled, use `AUTH=()`.

```bash
AUTH=()
```

## 3) Minimal working requests

1. Get device info (identity / model / generation)

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Shelly.GetDeviceInfo"}' \
  "http://${SHELLY}/rpc"
```

Expected keys in response: `name`, `id`, `mac`, `model`, `gen`, `fw_id`.

2. Get full device status

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Shelly.GetStatus"}' \
  "http://${SHELLY}/rpc"
```

Expected: top-level component statuses (including `switch:0` on devices with relay channel 0).

3. Get switch status (`id=0`)

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.GetStatus","params":{"id":0}}' \
  "http://${SHELLY}/rpc"
```

Expected keys: `id`, `source`, `output`.

4. Turn relay ON (`id=0`)

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.Set","params":{"id":0,"on":true}}' \
  "http://${SHELLY}/rpc"
```

Expected: success frame with matching request `id`.

5. Verify relay state after ON

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.GetStatus","params":{"id":0}}' \
  "http://${SHELLY}/rpc"
```

Expected: `"output": true`.

6. Turn relay OFF (`id=0`)

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.Set","params":{"id":0,"on":false}}' \
  "http://${SHELLY}/rpc"
```

Expected: success frame with matching request `id`.

7. Verify relay state after OFF

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.GetStatus","params":{"id":0}}' \
  "http://${SHELLY}/rpc"
```

Expected: `"output": false`.

## 4) Negative test (invalid switch id)

Use a non-existing relay id (example: `id=7`):

```bash
curl "${AUTH[@]}" -X POST \
  -d '{"id":1,"method":"Switch.GetStatus","params":{"id":7}}' \
  "http://${SHELLY}/rpc"
```

Expected error object shape:

```json
{
  "error": {
    "code": -105,
    "message": "Bad id=7"
  }
}
```

Another common argument error is `-103` (example message: `Missing required 'id'`).

## 5) Doc pointers in this local snapshot

- RPC channels and endpoint patterns:
  - `shelly-api-docs.shelly.cloud/gen2/General/RPCChannels/index.html`
- Shelly component methods (`Shelly.GetStatus`, `Shelly.GetDeviceInfo`):
  - `shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly/index.html`
- Switch methods (`Switch.Set`, `Switch.GetStatus`):
  - `shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch/index.html`
- Common error codes (`-103`, `-105`):
  - `shelly-api-docs.shelly.cloud/gen2/General/CommonErrors/index.html`
