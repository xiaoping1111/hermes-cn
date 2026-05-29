"""OpenRouter API 共享客户端

【产品经理理解要点】
为需要调用 OpenRouter 的工具（如 MoA）提供统一的 HTTP 客户端，避免重复创建连接和认证逻辑。
- 核心职责：懒初始化一个复用的异步 OpenAI 兼容客户端，统一处理 API Key 和路由
- 关键业务概念：单例复用——首次调用时创建客户端，后续共用；通过集中式路由器处理认证
- 在系统中的位置：mixture_of_agents_tool 等需要多模型调用的工具的基础设施

─────────────────────────────────────────────────────────────────
Shared OpenRouter API client for Hermes tools.

Provides a single lazy-initialized AsyncOpenAI client that all tool modules
can share.  Routes through the centralized provider router in
agent/auxiliary_client.py so auth, headers, and API format are handled
consistently.
"""

import os

_client = None


def get_async_client():
    """Return a shared async OpenAI-compatible client for OpenRouter.

    The client is created lazily on first call and reused thereafter.
    Uses the centralized provider router for auth and client construction.
    Raises ValueError if OPENROUTER_API_KEY is not set.
    """
    global _client
    if _client is None:
        from agent.auxiliary_client import resolve_provider_client
        client, _model = resolve_provider_client("openrouter", async_mode=True)
        if client is None:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        _client = client
    return _client


def check_api_key() -> bool:
    """Check whether the OpenRouter API key is present."""
    return bool(os.getenv("OPENROUTER_API_KEY"))
