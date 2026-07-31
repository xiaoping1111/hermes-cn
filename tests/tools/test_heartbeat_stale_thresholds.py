"""工具系统测试 - heartbeat stale thresholds

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的heartbeat stale thresholds验证。
- 验证功能：heartbeat stale thresholds功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：heartbeat stale thresholds功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for delegate heartbeat stale threshold configuration.
"""


class TestHeartbeatStaleThresholds:
    """Verify the heartbeat stale threshold constants are correct."""

    def test_idle_cycles_value(self):
        """IDLE stale cycles should be 15 (15 * 30s = 450s)."""
        from tools.delegate_tool import _HEARTBEAT_STALE_CYCLES_IDLE
        assert _HEARTBEAT_STALE_CYCLES_IDLE == 15

    def test_in_tool_cycles_value(self):
        """IN_TOOL stale cycles should be 40 (40 * 30s = 1200s)."""
        from tools.delegate_tool import _HEARTBEAT_STALE_CYCLES_IN_TOOL
        assert _HEARTBEAT_STALE_CYCLES_IN_TOOL == 40


    def test_in_tool_timeout_seconds(self):
        """Effective in-tool stale timeout: 40 * 30 = 1200s (= 20 minutes)."""
        from tools.delegate_tool import _HEARTBEAT_STALE_CYCLES_IN_TOOL, _HEARTBEAT_INTERVAL
        effective = _HEARTBEAT_STALE_CYCLES_IN_TOOL * _HEARTBEAT_INTERVAL
        assert effective == 1200

    def test_interval_unchanged(self):
        """Heartbeat interval should remain 30s."""
        from tools.delegate_tool import _HEARTBEAT_INTERVAL
        assert _HEARTBEAT_INTERVAL == 30
