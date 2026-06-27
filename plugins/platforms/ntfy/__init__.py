"""ntfy 推送通知平台插件

【产品经理理解要点】
ntfy 平台插件入口，将 NtfyAdapter 注册到 Hermes 网关，适合轻量通知场景。
"""

from .adapter import register

__all__ = ["register"]
