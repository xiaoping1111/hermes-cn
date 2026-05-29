"""Google Chat平台适配器插件入口

【产品经理理解要点】
Google Chat插件的注册入口，将Google Chat适配器接入Hermes网关系统。
- 核心职责：注册Google Chat平台适配器到Hermes插件系统
- 平台能力：在Google Chat空间和私聊中收发消息
"""

from .adapter import register

__all__ = ["register"]
