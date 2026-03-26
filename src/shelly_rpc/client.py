"""Shelly local RPC client.

Implements HTTP JSON-RPC calls against Shelly local endpoint `/rpc`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import count
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import (
    HTTPDigestAuthHandler,
    HTTPPasswordMgrWithDefaultRealm,
    Request,
    build_opener,
)

from .exceptions import ShellyRpcError, ShellyTransportError
from .types import RpcParams, RpcResult


@dataclass(slots=True)
class ShellyClientConfig:
    host: str
    username: str | None = None
    password: str | None = None
    use_https: bool = False
    timeout: float = 10.0


class ShellyClient:
    """Client for Shelly Gen2+/Gen3/Gen4 local RPC over HTTP."""

    def __init__(
        self,
        host: str,
        *,
        username: str | None = None,
        password: str | None = None,
        use_https: bool = False,
        timeout: float = 10.0,
    ) -> None:
        self.config = ShellyClientConfig(
            host=host,
            username=username,
            password=password,
            use_https=use_https,
            timeout=timeout,
        )
        self._id_seq = count(1)
        self._base_url = self._build_base_url(host, use_https)
        self._opener = self._build_opener()

    @staticmethod
    def _build_base_url(host: str, use_https: bool) -> str:
        cleaned = host.strip().rstrip("/")
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            return cleaned
        scheme = "https" if use_https else "http"
        return f"{scheme}://{cleaned}"

    def _build_opener(self):
        if self.config.username is None or self.config.password is None:
            return build_opener()

        mgr = HTTPPasswordMgrWithDefaultRealm()
        mgr.add_password(
            realm=None,
            uri=f"{self._base_url}/",
            user=self.config.username,
            passwd=self.config.password,
        )
        digest_handler = HTTPDigestAuthHandler(mgr)
        return build_opener(digest_handler)

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        req = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with self._opener.open(req, timeout=self.config.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except HTTPError as exc:
            msg = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
            raise ShellyTransportError(f"HTTP error {exc.code}: {msg}") from exc
        except URLError as exc:
            raise ShellyTransportError(f"Connection error: {exc.reason}") from exc
        except OSError as exc:
            raise ShellyTransportError(f"Transport error: {exc}") from exc

        try:
            parsed: dict[str, Any] = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ShellyTransportError("Invalid JSON response from Shelly device") from exc
        return parsed

    def call(self, method: str, params: RpcParams | None = None) -> RpcResult:
        """Call an RPC method via POST /rpc JSON-RPC frame and return result."""
        payload: dict[str, Any] = {"id": next(self._id_seq), "method": method}
        if params is not None:
            payload["params"] = params

        frame = self._post_json(f"{self._base_url}/rpc", payload)

        if "error" in frame:
            raise ShellyRpcError.from_error_object(frame["error"])

        if "result" in frame:
            return frame["result"]

        # Some endpoints may return object directly without wrapping in "result".
        return frame

    def call_method_endpoint(self, method: str, params: RpcParams | None = None) -> RpcResult:
        """Call method-specific endpoint POST /rpc/<method> with params object payload."""
        payload = params or {}
        frame = self._post_json(f"{self._base_url}/rpc/{method}", payload)

        if isinstance(frame, dict) and "error" in frame:
            raise ShellyRpcError.from_error_object(frame["error"])

        return frame

    # Convenience helpers for common Shelly/Switch operations.
    def get_device_info(self) -> RpcResult:
        return self.call("Shelly.GetDeviceInfo")

    def get_status(self) -> RpcResult:
        return self.call("Shelly.GetStatus")

    def switch_get_status(self, switch_id: int = 0) -> RpcResult:
        return self.call("Switch.GetStatus", {"id": switch_id})

    def switch_set(self, switch_id: int, on: bool) -> RpcResult:
        return self.call("Switch.Set", {"id": switch_id, "on": on})

    def switch_toggle(self, switch_id: int) -> RpcResult:
        return self.call("Switch.Toggle", {"id": switch_id})
