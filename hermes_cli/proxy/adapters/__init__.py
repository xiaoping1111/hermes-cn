"""代理适配器注册表

【产品经理理解要点】
注册和查找可用的上游代理适配器。
- ADAPTERS字典：适配器名→类的映射
- 每个适配器封装一个OAuth提供商的认证状态
- 新增提供商只需新增适配器类

────────────────────────────────────────────────────────────────
Upstream adapter registry for the local proxy server.

Each adapter wraps a provider's OAuth state and exposes a uniform interface
the proxy server can use to forward requests with a freshly-minted bearer
token. See :class:`UpstreamAdapter` for the contract."""

from typing import Dict, Type

from hermes_cli.proxy.adapters.base import UpstreamAdapter
from hermes_cli.proxy.adapters.nous_portal import NousPortalAdapter
from hermes_cli.proxy.adapters.xai import XAIGrokAdapter

# Registry of available adapter classes keyed by provider name as used on
# the ``hermes proxy start --provider <name>`` CLI flag.
ADAPTERS: Dict[str, Type[UpstreamAdapter]] = {
    "nous": NousPortalAdapter,
    "xai": XAIGrokAdapter,
}


def get_adapter(name: str) -> UpstreamAdapter:
    """Instantiate an adapter by provider name.

    Raises:
        ValueError: if ``name`` is not a registered adapter.
    """
    key = (name or "").strip().lower()
    if key not in ADAPTERS:
        available = ", ".join(sorted(ADAPTERS)) or "(none)"
        raise ValueError(
            f"Unknown proxy upstream provider: {name!r}. Available: {available}"
        )
    return ADAPTERS[key]()


__all__ = ["UpstreamAdapter", "ADAPTERS", "get_adapter"]
