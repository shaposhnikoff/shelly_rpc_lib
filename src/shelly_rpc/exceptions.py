"""Exception hierarchy for Shelly RPC client."""

from __future__ import annotations


class ShellyError(Exception):
    """Base class for all library errors."""


class ShellyTransportError(ShellyError):
    """Raised when HTTP transport fails or response is invalid."""


class ShellyRpcError(ShellyError):
    """Raised when Shelly returns an RPC-level error object."""

    def __init__(self, code: int, message: str, data: object | None = None):
        super().__init__(f"Shelly RPC error {code}: {message}")
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def from_error_object(cls, error_obj: dict) -> "ShellyRpcError":
        return cls(
            code=int(error_obj.get("code", -1)),
            message=str(error_obj.get("message", "Unknown RPC error")),
            data=error_obj.get("data"),
        )
