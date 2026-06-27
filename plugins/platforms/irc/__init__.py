"""IRC 平台插件

【产品经理理解要点】
IRC 平台插件入口，将 IRCAdapter 注册到 Hermes 网关，适用于技术社区场景。
"""

from .adapter import register

__all__ = ["register"]
