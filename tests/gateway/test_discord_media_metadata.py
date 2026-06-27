"""Discord网关测试

【产品经理理解要点】
Discord平台网关功能测试。
- 验证功能：Discord平台消息网关适配
- 关键场景：消息收发、连接管理、错误处理
- 业务影响：Discord平台功能不可用"""

import inspect

from plugins.platforms.discord.adapter import DiscordAdapter


def test_discord_media_methods_accept_metadata_kwarg():
    for method_name in ("send_voice", "send_image_file", "send_image"):
        signature = inspect.signature(getattr(DiscordAdapter, method_name))
        assert "metadata" in signature.parameters, method_name
