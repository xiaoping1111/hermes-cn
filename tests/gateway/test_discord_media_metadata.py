"""消息网关测试 - Discord平台·媒体处理·metadata

【产品经理理解要点】
验证消息网关的Discord平台媒体处理功能
- 验证的功能: Discord媒体消息元数据处理
- 核心测试场景: discord media methods accept metadata kwarg
- 业务影响: 消息网关可能出现命令丢失或平台适配错误，影响所有平台用户

─────────────────────────────────────────────────────────────────
消息网关测试 - Discord平台适配·媒体消息处理·metadata

测试多平台消息接入与命令分发中discord相关的media相关的metadata功能
"""

import inspect

from gateway.platforms.discord import DiscordAdapter


def test_discord_media_methods_accept_metadata_kwarg():
    for method_name in ("send_voice", "send_image_file", "send_image"):
        signature = inspect.signature(getattr(DiscordAdapter, method_name))
        assert "metadata" in signature.parameters, method_name
