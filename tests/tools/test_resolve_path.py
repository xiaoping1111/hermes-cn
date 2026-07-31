"""工具系统测试 - resolve path

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的resolve path验证。
- 验证功能：resolve path功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：resolve path功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for _resolve_path() — TERMINAL_CWD-aware path resolution in file_tools.
"""

import os
from pathlib import Path
from types import SimpleNamespace


class TestResolvePath:
    """Verify _resolve_path respects TERMINAL_CWD for worktree isolation."""

    def test_relative_path_uses_terminal_cwd(self, monkeypatch, tmp_path):
        """Relative paths resolve against TERMINAL_CWD, not process CWD."""
        monkeypatch.setenv("TERMINAL_CWD", str(tmp_path))
        from tools.file_tools import _resolve_path

        result = _resolve_path("foo/bar.py")
        assert result == (tmp_path / "foo" / "bar.py")


    def test_relative_path_prefers_recorded_session_cwd(self, monkeypatch, tmp_path):
        """The session's recorded cwd must win after the terminal changes directory."""
        start_dir = tmp_path / "start"
        live_dir = tmp_path / "worktree"
        start_dir.mkdir()
        live_dir.mkdir()
        monkeypatch.setenv("TERMINAL_CWD", str(start_dir))

        from tools import file_tools, terminal_tool

        task_id = "live-cwd"
        # The session's completed `cd` recorded the new directory.
        terminal_tool.record_session_cwd(task_id, str(live_dir))

        try:
            result = file_tools._resolve_path("nested/file.txt", task_id=task_id)
        finally:
            terminal_tool.clear_session_cwd(task_id)

        assert result == live_dir / "nested" / "file.txt"
