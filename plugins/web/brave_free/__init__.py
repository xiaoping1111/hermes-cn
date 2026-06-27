"""Brave 免费搜索插件

【产品经理理解要点】
Brave Search 免费层搜索后端入口。
- 无需 API Key 的 Brave Search 集成

─────────────────────────────────────────────────────────────────
Brave Search (free tier) plugin — bundled, auto-loaded.

Mirrors the ``plugins/image_gen/openai/`` layout: ``provider.py`` holds the
provider class, ``__init__.py::register(ctx)`` registers an instance.
"""

from __future__ import annotations

from plugins.web.brave_free.provider import BraveFreeWebSearchProvider


def register(ctx) -> None:
    """Register the Brave-free provider with the plugin context."""
    ctx.register_web_search_provider(BraveFreeWebSearchProvider())
