"""Raft 频道平台插件

【产品经理理解要点】
Raft 平台插件入口，将 RaftAdapter 注册到 Hermes 网关。
"""

from .adapter import register

__all__ = ["register"]
