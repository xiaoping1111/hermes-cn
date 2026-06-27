"""Home Assistant 智能家居平台插件

【产品经理理解要点】
Home Assistant 平台插件入口，将 HomeAssistantAdapter 注册到 Hermes 网关。
- 让 Agent 能感知和控制 Home Assistant 中的智能设备
"""

from .adapter import register

__all__ = ["register"]
