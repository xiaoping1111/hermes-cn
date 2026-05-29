"""Brave免费搜索插件 — 自动加载

【产品经理理解要点】
Brave Search免费版插件的注册入口。提供免费的网络搜索能力，每月2000次查询。
- 核心职责：将Brave免费版供应商注册到Hermes的搜索调度系统
- 仅搜索：不支持内容提取，需搭配其他提取供应商
- 免费额度：每月2000次查询，每秒1次

─────────────────────────────────────────────────────────────────
Mirrors the ``plugins/image_gen/openai/`` layout: ``provider.py`` holds the
provider class, ``__init__.py::register(ctx)`` registers an instance.
"""

from __future__ import annotations

from plugins.web.brave_free.provider import BraveFreeWebSearchProvider


def register(ctx) -> None:
    """Register the Brave-free provider with the plugin context."""
    ctx.register_web_search_provider(BraveFreeWebSearchProvider())
