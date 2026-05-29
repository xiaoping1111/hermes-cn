"""命令行界面测试 - Slack平台·CLI命令

【产品经理理解要点】
验证命令行界面的Slack平台CLI命令功能
- 验证的功能: Tests for Slack CLI helpers
- 核心测试场景: app home messages are writable、private channel directory scope is included、assistant features remain enabled
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Tests for Slack CLI helpers.
"""

from hermes_cli.slack_cli import _build_full_manifest


class TestSlackFullManifest:
    """Generated full Slack app manifest used by `hermes slack manifest`."""

    def test_app_home_messages_are_writable(self):
        manifest = _build_full_manifest("Hermes", "Your Hermes agent on Slack")

        assert manifest["features"]["app_home"] == {
            "home_tab_enabled": False,
            "messages_tab_enabled": True,
            "messages_tab_read_only_enabled": False,
        }

    def test_private_channel_directory_scope_is_included(self):
        manifest = _build_full_manifest("Hermes", "Your Hermes agent on Slack")

        bot_scopes = manifest["oauth_config"]["scopes"]["bot"]
        assert "groups:read" in bot_scopes

    def test_assistant_features_remain_enabled(self):
        manifest = _build_full_manifest("Hermes", "Your Hermes agent on Slack")

        assert "assistant_view" in manifest["features"]
        assert "assistant:write" in manifest["oauth_config"]["scopes"]["bot"]
        bot_events = manifest["settings"]["event_subscriptions"]["bot_events"]
        assert "assistant_thread_started" in bot_events
