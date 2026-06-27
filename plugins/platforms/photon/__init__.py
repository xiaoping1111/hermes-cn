"""Photon Spectrum (iMessage) 平台插件

【产品经理理解要点】
Photon/iMessage 平台插件入口，将 PhotonAdapter 注册到 Hermes 网关，实现 iMessage 收发。
"""

from .adapter import register

__all__ = ["register"]
