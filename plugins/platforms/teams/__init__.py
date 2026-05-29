"""Microsoft Teams平台适配器插件入口

【产品经理理解要点】
Microsoft Teams消息平台插件的注册入口，将Teams适配器接入Hermes网关系统。
- 核心职责：注册Teams平台适配器到Hermes插件系统
- 平台能力：收发消息、发送审批卡片、Typing指示、图片发送
"""

from .adapter import register

__all__ = ["register"]
