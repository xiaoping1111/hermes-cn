"""消息网关测试 - Webhook动态路由

【产品经理理解要点】
验证消息网关Webhook动态路由的正确性
- 验证的功能: Tests for webhook adapter dynamic route loading
- 核心测试场景: no dynamic file、loads dynamic routes、static takes precedence 等共6个场景
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
Tests for webhook adapter dynamic route loading.
"""

import json
import os
import pytest
from pathlib import Path

from gateway.config import PlatformConfig
from gateway.platforms.webhook import WebhookAdapter, _DYNAMIC_ROUTES_FILENAME


def _make_adapter(routes=None, extra=None):
    _extra = extra or {}
    if routes:
        _extra["routes"] = routes
    _extra.setdefault("secret", "test-global-secret")
    config = PlatformConfig(enabled=True, extra=_extra)
    return WebhookAdapter(config)


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))


class TestDynamicRouteLoading:
    def test_no_dynamic_file(self):
        adapter = _make_adapter(routes={"static": {"secret": "s"}})
        adapter._reload_dynamic_routes()
        assert "static" in adapter._routes
        assert len(adapter._dynamic_routes) == 0

    def test_loads_dynamic_routes(self, tmp_path):
        subs = {"my-hook": {"secret": "dynamic-secret", "prompt": "test", "events": []}}
        (tmp_path / _DYNAMIC_ROUTES_FILENAME).write_text(json.dumps(subs))

        adapter = _make_adapter(routes={"static": {"secret": "s"}})
        adapter._reload_dynamic_routes()
        assert "my-hook" in adapter._routes
        assert "static" in adapter._routes

    def test_static_takes_precedence(self, tmp_path):
        (tmp_path / _DYNAMIC_ROUTES_FILENAME).write_text(
            json.dumps({"conflict": {"secret": "dynamic", "prompt": "dyn"}})
        )
        adapter = _make_adapter(routes={"conflict": {"secret": "static", "prompt": "stat"}})
        adapter._reload_dynamic_routes()
        assert adapter._routes["conflict"]["secret"] == "static"

    def test_mtime_gated(self, tmp_path):
        import time
        path = tmp_path / _DYNAMIC_ROUTES_FILENAME
        path.write_text(json.dumps({"v1": {"secret": "s"}}))

        adapter = _make_adapter()
        adapter._reload_dynamic_routes()
        assert "v1" in adapter._dynamic_routes

        # Same mtime — no reload
        adapter._dynamic_routes["injected"] = True
        adapter._reload_dynamic_routes()
        assert "injected" in adapter._dynamic_routes

        # New write — reloads
        time.sleep(0.05)
        path.write_text(json.dumps({"v2": {"secret": "s"}}))
        adapter._reload_dynamic_routes()
        assert "v2" in adapter._dynamic_routes
        assert "v1" not in adapter._dynamic_routes

    def test_file_removal_clears(self, tmp_path):
        path = tmp_path / _DYNAMIC_ROUTES_FILENAME
        path.write_text(json.dumps({"temp": {"secret": "s"}}))
        adapter = _make_adapter()
        adapter._reload_dynamic_routes()
        assert "temp" in adapter._dynamic_routes

        path.unlink()
        adapter._reload_dynamic_routes()
        assert len(adapter._dynamic_routes) == 0

    def test_corrupted_file(self, tmp_path):
        (tmp_path / _DYNAMIC_ROUTES_FILENAME).write_text("not json")
        adapter = _make_adapter(routes={"static": {"secret": "s"}})
        adapter._reload_dynamic_routes()
        assert "static" in adapter._routes
        assert len(adapter._dynamic_routes) == 0
