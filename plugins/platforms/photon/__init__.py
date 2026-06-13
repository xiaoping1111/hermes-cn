"""Photon Spectrum (iMessage) platform plugin entry point.

【产品经理理解要点】
平台插件——额外的即时通讯平台对接（__init__.py）
"""

from .adapter import register

__all__ = ["register"]
