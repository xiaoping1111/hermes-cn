"""IRC平台适配器插件入口

【产品经理理解要点】
IRC（Internet Relay Chat）插件的注册入口，将IRC适配器接入Hermes网关系统。
- 核心职责：注册IRC平台适配器到Hermes插件系统
- 平台特点：经典文本聊天协议，零外部依赖（纯Python标准库实现）
"""

from .adapter import register

__all__ = ["register"]
