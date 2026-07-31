"""Discord网关测试

【产品经理理解要点】
Discord平台网关功能测试。
- 验证功能：Discord平台消息网关适配
- 关键场景：消息收发、连接管理、错误处理
- 业务影响：Discord平台功能不可用

─────────────────────────────────────────────────────────────────────────
Tests for Discord Opus codec loading — must use ctypes.util.find_library."""

import inspect
import types


class TestOpusFindLibrary:
    """Opus loading must try ctypes.util.find_library first, with platform fallback."""

    def test_uses_find_library_first(self):
        """find_library must be the primary lookup strategy."""
        from plugins.platforms.discord.adapter import DiscordAdapter
        source = inspect.getsource(DiscordAdapter.connect)
        assert "find_library" in source, \
            "Opus loading must use ctypes.util.find_library"


