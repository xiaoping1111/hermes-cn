"""Mattermost 平台插件

【产品经理理解要点】
Mattermost 平台插件入口，将 MattermostAdapter 注册到 Hermes 网关，面向企业自建场景。
"""

from .adapter import register

__all__ = ["register"]
