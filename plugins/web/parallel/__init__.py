"""Parallel.ai搜索+提取插件 — 自动加载

【产品经理理解要点】
Parallel.ai插件的注册入口。首个支持异步内容提取的插件，搜索和提取使用不同的SDK客户端。
- 核心职责：将Parallel供应商注册到Hermes的搜索调度系统
- 双能力：搜索(同步) + 内容提取(异步)
- 技术亮点：首个使用异步extract方法的插件，调度器自动检测并await

─────────────────────────────────────────────────────────────────
First plugin in this repo to expose an async :meth:`extract` — Parallel's
SDK is async-native (``AsyncParallel.beta.extract``). The web_extract_tool
dispatcher detects coroutines via :func:`inspect.iscoroutinefunction` and
awaits.
"""

from __future__ import annotations

from plugins.web.parallel.provider import ParallelWebSearchProvider


def register(ctx) -> None:
    """Register the Parallel provider with the plugin context."""
    ctx.register_web_search_provider(ParallelWebSearchProvider())
