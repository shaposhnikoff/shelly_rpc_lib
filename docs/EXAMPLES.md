# Usage Examples

## 1) Basic health check

```python
from shelly_rpc import ShellyClient

client = ShellyClient("192.168.33.1")

info = client.get_device_info()
status = client.get_status()

print("Device:", info.get("model"), info.get("id"))
print("Uptime:", status.get("sys", {}).get("uptime"))
```

## 2) Relay on/off flow

```python
from shelly_rpc import ShellyClient

client = ShellyClient("192.168.33.1")

before = client.switch_get_status(0)
print("Before:", before.get("output"))

client.switch_set(0, True)
after_on = client.switch_get_status(0)
print("After ON:", after_on.get("output"))

client.switch_set(0, False)
after_off = client.switch_get_status(0)
print("After OFF:", after_off.get("output"))
```

## 3) Use method endpoint `/rpc/<method>`

```python
from shelly_rpc import ShellyClient

client = ShellyClient("192.168.33.1")

# Equivalent to POST /rpc/Switch.Set with body {"id": 0, "on": true}
result = client.call_method_endpoint("Switch.Set", {"id": 0, "on": True})
print(result)
```

## 4) Auth-enabled device

```python
from shelly_rpc import ShellyClient

client = ShellyClient(
    "192.168.33.1",
    username="admin",
    password="secret",
)

print(client.get_device_info())
```

## 5) Robust error handling

```python
from shelly_rpc import ShellyClient, ShellyRpcError, ShellyTransportError

client = ShellyClient("192.168.33.1")

try:
    # Non-existing switch id, typical RPC error -105.
    client.switch_get_status(7)
except ShellyRpcError as e:
    print("RPC:", e.code, e.message)
except ShellyTransportError as e:
    print("Transport:", e)
```

## 6) Generic call for methods not wrapped yet

```python
from shelly_rpc import ShellyClient

client = ShellyClient("192.168.33.1")

methods = client.call("Shelly.ListMethods")
print(methods)
```
