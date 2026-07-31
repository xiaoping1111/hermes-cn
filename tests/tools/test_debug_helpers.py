"""工具系统测试 - debug helpers

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的debug helpers验证。
- 验证功能：debug helpers功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：debug helpers功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for tools/debug_helpers.py — DebugSession class.
"""

import json
import os
from unittest.mock import patch

from tools.debug_helpers import DebugSession


class TestDebugSessionDisabled:
    """When the env var is not set, DebugSession should be a cheap no-op."""

    def test_not_active_by_default(self):
        ds = DebugSession("test_tool", env_var="FAKE_DEBUG_VAR_XYZ")
        assert ds.active is False
        assert ds.enabled is False


    def test_get_session_info_disabled(self):
        ds = DebugSession("test_tool", env_var="FAKE_DEBUG_VAR_XYZ")
        info = ds.get_session_info()
        assert info["enabled"] is False
        assert info["session_id"] is None
        assert info["log_path"] is None
        assert info["total_calls"] == 0


class TestDebugSessionEnabled:
    """When the env var is set to 'true', DebugSession records and saves."""

    def _make_enabled(self, tmp_path):
        with patch.dict(os.environ, {"TEST_DEBUG": "true"}):
            ds = DebugSession("test_tool", env_var="TEST_DEBUG")
        ds.log_dir = tmp_path
        return ds

    def test_active_when_env_set(self, tmp_path):
        ds = self._make_enabled(tmp_path)
        assert ds.active is True
        assert ds.enabled is True

    def test_session_id_generated(self, tmp_path):
        ds = self._make_enabled(tmp_path)
        assert len(ds.session_id) > 0


    def test_save_empty_log(self, tmp_path):
        ds = self._make_enabled(tmp_path)
        ds.save()
        files = list(tmp_path.glob("*.json"))
        assert len(files) == 1
        data = json.loads(files[0].read_text())
        assert data["total_calls"] == 0
        assert data["tool_calls"] == []
