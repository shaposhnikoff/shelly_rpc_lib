"""Type aliases used by shelly_rpc."""

from __future__ import annotations

from typing import Any

RpcParams = dict[str, Any]
RpcResult = dict[str, Any] | list[Any] | str | int | float | bool | None
