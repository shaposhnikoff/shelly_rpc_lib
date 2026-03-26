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

## 7) Shelly 1PM Mini Gen3: relay + power telemetry

```python
from shelly_rpc import ShellyClient

# Replace with your Shelly 1PM Mini Gen3 IP/hostname.
client = ShellyClient("192.168.33.1")

# 1) Turn relay ON.
client.switch_set(0, True)

# 2) Read switch status and extract power metrics.
sw = client.switch_get_status(0)
print("Relay output:", sw.get("output"))
print("Source:", sw.get("source"))
print("Active power (W):", sw.get("apower"))
print("Voltage (V):", sw.get("voltage"))
print("Current (A):", sw.get("current"))
print("Total energy:", sw.get("aenergy"))

# 3) Turn relay OFF.
client.switch_set(0, False)
```

## 8) Shelly Plus 1: basic relay control

```python
from shelly_rpc import ShellyClient

# Replace with your Shelly Plus 1 IP/hostname.
client = ShellyClient("192.168.33.1")

# Check current relay state.
before = client.switch_get_status(0)
print("Before:", before.get("output"), "source:", before.get("source"))

# Turn relay ON and verify.
client.switch_set(0, True)
after_on = client.switch_get_status(0)
print("After ON:", after_on.get("output"))

# Toggle relay and verify.
client.switch_toggle(0)
after_toggle = client.switch_get_status(0)
print("After toggle:", after_toggle.get("output"))

# Turn relay OFF and verify.
client.switch_set(0, False)
after_off = client.switch_get_status(0)
print("After OFF:", after_off.get("output"))
```

## 9) Shelly Pro 3EM: energy metering snapshot

```python
from shelly_rpc import ShellyClient

# Replace with your Shelly Pro 3EM IP/hostname.
client = ShellyClient("192.168.33.1")

status = client.get_status()

# Typical components on Pro 3EM include em:0 and one or more emdata:* entries.
em = status.get("em:0", {})
phase_a = status.get("emdata:0", {})
phase_b = status.get("emdata:1", {})
phase_c = status.get("emdata:2", {})

print("Total active power (W):", em.get("total_act_power"))
print("Total active energy:", em.get("total_act"))
print("Total returned energy:", em.get("total_act_ret"))

print("Phase A power (W):", phase_a.get("act_power"))
print("Phase B power (W):", phase_b.get("act_power"))
print("Phase C power (W):", phase_c.get("act_power"))

print("Phase A voltage (V):", phase_a.get("voltage"))
print("Phase B voltage (V):", phase_b.get("voltage"))
print("Phase C voltage (V):", phase_c.get("voltage"))
```
