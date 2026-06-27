"""Microsoft Teams 平台插件

【产品经理理解要点】
Teams 平台插件入口，将 TeamsAdapter 注册到 Hermes 网关，面向企业 Teams 用户。
"""

from .adapter import register

__all__ = ["register"]
