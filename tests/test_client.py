from __future__ import annotations

import unittest

from shelly_rpc import ShellyClient
from shelly_rpc.exceptions import ShellyRpcError


class ShellyClientTests(unittest.TestCase):
    def test_base_url_is_normalized(self):
        c1 = ShellyClient("192.168.1.10")
        self.assertEqual(c1._base_url, "http://192.168.1.10")

        c2 = ShellyClient("https://example.local/")
        self.assertEqual(c2._base_url, "https://example.local")

    def test_call_returns_result_field(self):
        client = ShellyClient("192.168.1.10")
        client._post_json = lambda _url, _payload: {"id": 1, "result": {"ok": True}}  # type: ignore[attr-defined]

        result = client.call("Shelly.GetStatus")
        self.assertEqual(result, {"ok": True})

    def test_call_returns_frame_when_result_absent(self):
        client = ShellyClient("192.168.1.10")
        client._post_json = lambda _url, _payload: {"id": 1, "output": False}  # type: ignore[attr-defined]

        result = client.call("Switch.GetStatus", {"id": 0})
        self.assertEqual(result, {"id": 1, "output": False})

    def test_call_raises_rpc_error(self):
        client = ShellyClient("192.168.1.10")
        client._post_json = lambda _url, _payload: {  # type: ignore[attr-defined]
            "error": {"code": -105, "message": "Bad id=7"}
        }

        with self.assertRaises(ShellyRpcError) as ctx:
            client.call("Switch.GetStatus", {"id": 7})

        self.assertEqual(ctx.exception.code, -105)
        self.assertEqual(ctx.exception.message, "Bad id=7")

    def test_switch_set_uses_expected_method_and_params(self):
        client = ShellyClient("192.168.1.10")
        captured = {}

        def fake_post(_url, payload):
            captured["payload"] = payload
            return {"id": payload["id"], "result": {"was_on": False}}

        client._post_json = fake_post  # type: ignore[attr-defined]

        client.switch_set(0, True)
        self.assertEqual(captured["payload"]["method"], "Switch.Set")
        self.assertEqual(captured["payload"]["params"], {"id": 0, "on": True})


if __name__ == "__main__":
    unittest.main()
