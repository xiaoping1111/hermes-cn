"""命令行界面测试 - 强制刷新

【产品经理理解要点】
验证命令行界面强制刷新的正确性
- 验证的功能: Regression: ``hermes setup`` for the ollama-cloud provider must force-refresh
- 核心测试场景: setup ollama cloud passes force refresh
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Regression: ``hermes setup`` for the ollama-cloud provider must force-refresh
the model cache after the user supplies a key, otherwise the picker keeps
serving a stale cache (models.dev only, no live API probe) for up to an hour.
"""

from __future__ import annotations

from unittest.mock import patch


def test_setup_ollama_cloud_passes_force_refresh(monkeypatch):
    """The provider-setup model-fetch for ollama-cloud must pass ``force_refresh=True``."""
    import hermes_cli.main as main_mod
    import inspect

    src = inspect.getsource(main_mod)

    # Locate the ollama-cloud branch in the provider setup flow.
    marker = 'provider_id == "ollama-cloud"'
    assert marker in src, "ollama-cloud branch missing from provider setup"
    idx = src.index(marker)
    # The call to fetch_ollama_cloud_models should be within the next ~2000 chars.
    snippet = src[idx:idx + 2000]
    assert "fetch_ollama_cloud_models(" in snippet, snippet[:500]
    assert "force_refresh=True" in snippet, (
        "ollama-cloud setup must pass force_refresh=True so newly released "
        "models (e.g. deepseek v4 flash, kimi k2.6) appear the moment the "
        "user enters their key, not an hour later when the cache TTL expires. "
        f"Snippet: {snippet[:500]}"
    )
