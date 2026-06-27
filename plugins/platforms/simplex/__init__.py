"""SimpleX 隐私聊天平台插件

【产品经理理解要点】
SimpleX 平台插件入口，将 SimpleXAdapter 注册到 Hermes 网关，主打隐私通讯。
"""

from .adapter import register

__all__ = ["register"]
