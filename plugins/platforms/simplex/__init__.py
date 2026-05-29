"""SimpleX Chat平台适配器插件入口

【产品经理理解要点】
SimpleX Chat插件的注册入口，将SimpleX适配器接入Hermes网关系统。
- 核心职责：注册SimpleX平台适配器到Hermes插件系统
- 平台特点：去中心化、隐私优先的消息平台，通过WebSocket连接daemon
"""

from .adapter import register

__all__ = ["register"]
