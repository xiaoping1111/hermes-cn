"""Hermes 网关 — 多平台消息集成入口

【产品经理理解要点】
网关是 Agent 连接外部通讯平台的桥梁，让 AI 通过用户的日常聊天工具（Telegram、
Discord、微信、飞书等）与用户交互。核心能力：
  - 多平台统一接入：不同聊天平台用同一套代码处理
  - 会话管理：跨消息保持对话上下文，支持自动重置策略
  - 动态上下文注入：AI 知道消息来自哪个平台、哪个群组
  - 消息投递路由：定时任务的结果能自动发到正确的频道

─────────────────────────────────────────────────────────────────

Hermes Gateway - Multi-platform messaging integration.

This module provides a unified gateway for connecting the Hermes agent
to various messaging platforms (Telegram, Discord, WhatsApp, Weixin, and more) with:
- Session management (persistent conversations with reset policies)
- Dynamic context injection (agent knows where messages come from)
- Delivery routing (cron job outputs to appropriate channels)
- Platform-specific toolsets (different capabilities per platform)
"""

from .config import GatewayConfig, PlatformConfig, HomeChannel, load_gateway_config
from .session import (
    SessionContext,
    SessionStore,
    SessionResetPolicy,
    build_session_context_prompt,
)
from .delivery import DeliveryRouter, DeliveryTarget

__all__ = [
    # Config
    "GatewayConfig",
    "PlatformConfig", 
    "HomeChannel",
    "load_gateway_config",
    # Session
    "SessionContext",
    "SessionStore",
    "SessionResetPolicy",
    "build_session_context_prompt",
    # Delivery
    "DeliveryRouter",
    "DeliveryTarget",
]
