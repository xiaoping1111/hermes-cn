"""CLI终端测试 - cli mcp config watch

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的cli mcp config watch验证。
- 验证功能：cli mcp config watch功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：cli mcp config watch功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for automatic MCP reload when config.yaml mcp_servers section changes.
"""
import time
from pathlib import Path
from unittest.mock import MagicMock, patch


def _make_cli(tmp_path, mcp_servers=None):
    """Create a minimal HermesCLI instance with mocked config."""
    import cli as cli_mod
    obj = object.__new__(cli_mod.HermesCLI)
    obj.config = {"mcp_servers": mcp_servers or {}}
    obj._agent_running = False
    obj._last_config_check = 0.0
    obj._config_mcp_servers = mcp_servers or {}

    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("mcp_servers: {}\n")
    obj._config_mtime = cfg_file.stat().st_mtime

    obj._reload_mcp = MagicMock()
    obj._busy_command = MagicMock()
    obj._busy_command.return_value.__enter__ = MagicMock(return_value=None)
    obj._busy_command.return_value.__exit__ = MagicMock(return_value=False)
    obj._slow_command_status = MagicMock(return_value="reloading...")

    return obj, cfg_file


class TestMCPConfigWatch:

    def test_no_change_does_not_reload(self, tmp_path):
        """If mtime and mcp_servers unchanged, _reload_mcp is NOT called."""
        obj, cfg_file = _make_cli(tmp_path)

        with patch("hermes_cli.config.get_config_path", return_value=cfg_file):
            obj._check_config_mcp_changes()

        obj._reload_mcp.assert_not_called()

    def test_mtime_change_with_same_mcp_servers_does_not_reload(self, tmp_path):
        """If file mtime changes but mcp_servers is identical, no reload."""
        import yaml
        obj, cfg_file = _make_cli(tmp_path, mcp_servers={"fs": {"command": "npx"}})

        # Write same mcp_servers but touch the file
        cfg_file.write_text(yaml.dump({"mcp_servers": {"fs": {"command": "npx"}}}))
        # Force mtime to appear changed
        obj._config_mtime = 0.0

        with patch("hermes_cli.config.get_config_path", return_value=cfg_file):
            obj._check_config_mcp_changes()

        obj._reload_mcp.assert_not_called()

    def test_new_mcp_server_triggers_reload(self, tmp_path):
        """Adding a new MCP server to config triggers auto-reload."""
        import yaml
        obj, cfg_file = _make_cli(tmp_path, mcp_servers={})

        # Simulate user adding a new MCP server to config.yaml
        cfg_file.write_text(yaml.dump({"mcp_servers": {"github": {"url": "https://mcp.github.com"}}}))
        obj._config_mtime = 0.0  # force stale mtime

        with patch("hermes_cli.config.get_config_path", return_value=cfg_file):
            obj._check_config_mcp_changes()

        obj._reload_mcp.assert_called_once()

    def test_removed_mcp_server_triggers_reload(self, tmp_path):
        """Removing an MCP server from config triggers auto-reload."""
        import yaml
        obj, cfg_file = _make_cli(tmp_path, mcp_servers={"github": {"url": "https://mcp.github.com"}})

        # Simulate user removing the server
        cfg_file.write_text(yaml.dump({"mcp_servers": {}}))
        obj._config_mtime = 0.0

        with patch("hermes_cli.config.get_config_path", return_value=cfg_file):
            obj._check_config_mcp_changes()

        obj._reload_mcp.assert_called_once()

    def test_interval_throttle_skips_check(self, tmp_path):
        """If called within CONFIG_WATCH_INTERVAL, stat() is skipped."""
        obj, cfg_file = _make_cli(tmp_path)
        obj._last_config_check = time.monotonic()  # just checked

        with patch("hermes_cli.config.get_config_path", return_value=cfg_file), \
             patch.object(Path, "stat") as mock_stat:
            obj._check_config_mcp_changes()
            mock_stat.assert_not_called()

        obj._reload_mcp.assert_not_called()

    def test_missing_config_file_does_not_crash(self, tmp_path):
        """If config.yaml doesn't exist, _check_config_mcp_changes is a no-op."""
        obj, cfg_file = _make_cli(tmp_path)
        missing = tmp_path / "nonexistent.yaml"

        with patch("hermes_cli.config.get_config_path", return_value=missing):
            obj._check_config_mcp_changes()  # should not raise

        obj._reload_mcp.assert_not_called()
