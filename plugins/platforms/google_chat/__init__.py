"""Google Chat 平台插件

【产品经理理解要点】
Google Chat 平台插件入口，将 GoogleChatAdapter 注册到 Hermes 网关。
- 面向 Google Workspace 企业用户
"""

from .adapter import register

__all__ = ["register"]
