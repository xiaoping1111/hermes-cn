"""Discord 平台插件

【产品经理理解要点】
Discord 平台插件入口，将 DiscordAdapter 注册到 Hermes 网关。
- 用户在 Discord 服务器或私聊中与 Agent 交互
- 支持 Discord 特有功能：斜杠命令、反应反馈、语音频道等
"""

from .adapter import register

__all__ = ["register"]
