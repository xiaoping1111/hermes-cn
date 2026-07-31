"""Agent核心测试 - ssl ca guard

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的ssl ca guard验证。
- 验证功能：ssl ca guard功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：ssl ca guard功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for the preventive SSL CA bundle guard.
"""

from pathlib import Path

import certifi
import pytest

from agent.errors import SSLConfigurationError
from agent.ssl_guard import verify_ca_bundle, verify_ca_bundle_with_fallback


def test_healthy_bundle_passes(monkeypatch):
    """A real, non-empty certifi bundle must verify without raising."""
    for key in ("HERMES_CA_BUNDLE", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        monkeypatch.delenv(key, raising=False)
    bundle = Path(certifi.where())
    assert bundle.exists()
    assert bundle.stat().st_size > 1024
    verify_ca_bundle()




def test_empty_certifi_bundle_raises_ssl_error(monkeypatch, tmp_path):
    """Empty file is treated as a corrupted bundle."""
    fake = tmp_path / "empty.pem"
    fake.write_bytes(b"")
    monkeypatch.setattr(certifi, "where", lambda: str(fake))
    with pytest.raises(SSLConfigurationError) as exc:
        verify_ca_bundle()
    assert "too small" in str(exc.value).lower()


@pytest.mark.parametrize("env_var", ["HERMES_CA_BUNDLE", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"])
def test_missing_explicit_ca_bundle_env_raises_before_httpx(monkeypatch, tmp_path, env_var):
    """Bad CA-bundle env vars should be reported before OpenAI/httpx init."""
    fake = tmp_path / "missing.pem"
    monkeypatch.setenv(env_var, str(fake))
    with pytest.raises(SSLConfigurationError) as exc:
        verify_ca_bundle()
    message = str(exc.value)
    assert env_var in message
    assert str(fake) in message
    assert "force-reinstall" in message






