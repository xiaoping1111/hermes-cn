"""命令行界面测试 - 清除·stale·base·url

【产品经理理解要点】
验证命令行界面的清除功能
- 验证的功能: Tests for _clear_stale_openai_base_url() cleanup after provider switch (#5161)
- 核心测试场景: clears when provider is named、preserves when provider is custom、noop when no openai base url 等共4个场景
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Tests for _clear_stale_openai_base_url() cleanup after provider switch (#5161).
"""

from __future__ import annotations

from unittest.mock import patch

from hermes_cli.config import load_config, save_config, save_env_value, get_env_value


def _write_provider(provider: str, model: str = "test-model"):
    """Helper: write a provider + model to config.yaml."""
    cfg = load_config()
    model_cfg = cfg.get("model", {})
    if not isinstance(model_cfg, dict):
        model_cfg = {}
    model_cfg["provider"] = provider
    model_cfg["default"] = model
    cfg["model"] = model_cfg
    save_config(cfg)


class TestClearStaleOpenaiBaseUrl:
    """_clear_stale_openai_base_url() removes OPENAI_BASE_URL when provider is not custom."""

    def test_clears_when_provider_is_named(self, monkeypatch):
        """OPENAI_BASE_URL is cleared when config provider is a named provider."""
        from hermes_cli.main import _clear_stale_openai_base_url

        _write_provider("openrouter")
        save_env_value("OPENAI_BASE_URL", "http://localhost:11434/v1")

        _clear_stale_openai_base_url()

        result = get_env_value("OPENAI_BASE_URL")
        assert not result, f"Expected OPENAI_BASE_URL to be cleared, got: {result!r}"

    def test_preserves_when_provider_is_custom(self, monkeypatch):
        """OPENAI_BASE_URL is NOT cleared when config provider is 'custom'."""
        from hermes_cli.main import _clear_stale_openai_base_url

        _write_provider("custom")
        save_env_value("OPENAI_BASE_URL", "http://localhost:11434/v1")

        _clear_stale_openai_base_url()

        result = get_env_value("OPENAI_BASE_URL")
        assert result == "http://localhost:11434/v1", \
            f"Expected OPENAI_BASE_URL to be preserved, got: {result!r}"

    def test_noop_when_no_openai_base_url(self, monkeypatch):
        """No error when OPENAI_BASE_URL is not set."""
        from hermes_cli.main import _clear_stale_openai_base_url

        _write_provider("openrouter")
        # Ensure it's not set
        save_env_value("OPENAI_BASE_URL", "")
        monkeypatch.delenv("OPENAI_BASE_URL", raising=False)

        # Should not raise
        _clear_stale_openai_base_url()

    def test_noop_when_provider_empty(self, monkeypatch):
        """No cleanup when provider is not set in config."""
        from hermes_cli.main import _clear_stale_openai_base_url

        cfg = load_config()
        cfg.pop("model", None)
        save_config(cfg)
        save_env_value("OPENAI_BASE_URL", "http://localhost:11434/v1")

        _clear_stale_openai_base_url()

        result = get_env_value("OPENAI_BASE_URL")
        assert result == "http://localhost:11434/v1", \
            "Should not clear when provider is not configured"
