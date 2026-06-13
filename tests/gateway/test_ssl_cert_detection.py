"""Regression tests for gateway SSL certificate environment repair.

【产品经理理解要点】
网关测试——验证各平台消息收发和会话管理（test_ssl_cert_detection.py）
"""

from types import SimpleNamespace


def test_ensure_ssl_certs_ignores_stale_ssl_cert_file(monkeypatch, tmp_path):
    """A missing SSL_CERT_FILE should be treated as unset, not trusted."""
    import ssl
    import sys

    from gateway.run import _ensure_ssl_certs

    cert_file = tmp_path / "cacert.pem"
    cert_file.write_text("dummy cert bundle", encoding="utf-8")
    stale_file = tmp_path / "missing.pem"

    monkeypatch.setenv("SSL_CERT_FILE", str(stale_file))
    monkeypatch.setattr(
        ssl,
        "get_default_verify_paths",
        lambda: SimpleNamespace(cafile=None, openssl_cafile=None),
    )
    monkeypatch.setitem(
        sys.modules,
        "certifi",
        SimpleNamespace(where=lambda: str(cert_file)),
    )

    _ensure_ssl_certs()

    assert stale_file.exists() is False
    assert __import__("os").environ["SSL_CERT_FILE"] == str(cert_file)


def test_ensure_ssl_certs_keeps_existing_ssl_cert_file(monkeypatch, tmp_path):
    """A valid user-provided SSL_CERT_FILE must not be overwritten."""
    from gateway.run import _ensure_ssl_certs

    cert_file = tmp_path / "existing.pem"
    cert_file.write_text("dummy cert bundle", encoding="utf-8")
    monkeypatch.setenv("SSL_CERT_FILE", str(cert_file))

    _ensure_ssl_certs()

    assert __import__("os").environ["SSL_CERT_FILE"] == str(cert_file)