"""传输层注册中心

【产品经理理解要点】
统一管理所有AI供应商的格式转换适配器，让系统无需关心底层供应商差异。
- 维护一个"供应商名称→适配器"的注册表，按需加载对应适配器
- 新增供应商只需注册适配器，无需改动业务代码，支持渐进式迁移
- 是Hermes多模型支持能力的核心入口

─────────────────────────────────────────────────────────────────
Transport layer types and registry for provider response normalization.

Usage:
    from agent.transports import get_transport
    transport = get_transport("anthropic_messages")
    result = transport.normalize_response(raw_response)
"""

from agent.transports.types import (
    NormalizedResponse,
    ToolCall,
    Usage,
    build_tool_call,
    map_finish_reason,
)  # noqa: F401

_REGISTRY: dict = {}
_discovered: bool = False


def register_transport(api_mode: str, transport_cls: type) -> None:
    """Register a transport class for an api_mode string."""
    _REGISTRY[api_mode] = transport_cls


def get_transport(api_mode: str):
    """Get a transport instance for the given api_mode.

    Returns None if no transport is registered for this api_mode.
    This allows gradual migration — call sites can check for None
    and fall back to the legacy code path.
    """
    global _discovered
    if not _discovered:
        _discover_transports()
    cls = _REGISTRY.get(api_mode)
    if cls is None:
        # The registry can be partially populated when a specific transport
        # module was imported directly (for example chat_completions before
        # codex).  Discover on misses, not only when the registry is empty, so
        # test/order-dependent imports do not make valid api_modes unavailable.
        _discover_transports()
        cls = _REGISTRY.get(api_mode)
    if cls is None:
        return None
    return cls()


def _discover_transports() -> None:
    """Import all transport modules to trigger auto-registration."""
    global _discovered
    _discovered = True
    try:
        import agent.transports.anthropic  # noqa: F401
    except ImportError:
        pass
    try:
        import agent.transports.codex  # noqa: F401
    except ImportError:
        pass
    try:
        import agent.transports.chat_completions  # noqa: F401
    except ImportError:
        pass
    try:
        import agent.transports.bedrock  # noqa: F401
    except ImportError:
        pass
