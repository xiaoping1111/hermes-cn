"""LINE 消息平台插件

【产品经理理解要点】
LINE 平台插件入口，将 LINEAdapter 注册到 Hermes 网关，面向 LINE 用户群。
"""

from .adapter import register

__all__ = ["register"]
