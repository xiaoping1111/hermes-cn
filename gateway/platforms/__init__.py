"""平台适配器集合 — 各通讯平台的消息收发和认证实现

【产品经理理解要点】
每个平台适配器负责：
  - 接收来自平台的消息
  - 将 AI 回复发回平台
  - 处理平台特有的认证方式
  - 处理消息格式和媒体文件

支持的平台：Telegram、Discord、WhatsApp、微信、飞书、钉钉、企业微信、
Signal、Slack、Matrix、QQ、Email、元宝等。

─────────────────────────────────────────────────────────────────

Platform adapters for messaging integrations.

Each adapter handles:
- Receiving messages from a platform
- Sending messages/responses back
- Platform-specific authentication
- Message formatting and media handling
"""

from .base import BasePlatformAdapter, MessageEvent, SendResult

# QQAdapter and YuanbaoAdapter were previously imported eagerly here, but
# nothing in the codebase consumes ``from gateway.platforms import
# QQAdapter`` (every real call site uses the long-form path
# ``from gateway.platforms.qqbot import QQAdapter``). The eager imports
# pulled in qqbot's chunked-upload + keyboards + onboard machinery and
# yuanbao's websocket stack — about 48 ms wall and ~8 MB RSS on every
# CLI invocation, even ones that never touch a gateway adapter.
#
# Use PEP 562 module ``__getattr__`` to keep the public re-export working
# while deferring the actual import to first attribute access. This is
# 100% backward-compatible for any external code that still imports the
# adapters from the package root.
__all__ = [
    "BasePlatformAdapter",
    "MessageEvent",
    "SendResult",
    "QQAdapter",
    "YuanbaoAdapter",
]


def __getattr__(name):
    if name == "QQAdapter":
        from .qqbot import QQAdapter  # noqa: F401
        return QQAdapter
    if name == "YuanbaoAdapter":
        from .yuanbao import YuanbaoAdapter  # noqa: F401
        return YuanbaoAdapter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
