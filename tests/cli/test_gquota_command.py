from unittest.mock import MagicMock, patch
"""CLI终端测试 - gquota command

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的gquota command验证。
- 验证功能：gquota command功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：gquota command功能异常或存在安全隐患"""



def test_gquota_uses_chat_console_when_tui_is_live():
    from agent.google_oauth import GoogleOAuthError
    from cli import HermesCLI

    cli = HermesCLI.__new__(HermesCLI)
    cli.console = MagicMock()
    cli._app = object()

    live_console = MagicMock()

    with patch("cli.ChatConsole", return_value=live_console), \
         patch("agent.google_oauth.get_valid_access_token", side_effect=GoogleOAuthError("No Google OAuth credentials found")), \
         patch("agent.google_oauth.load_credentials", return_value=None), \
         patch("agent.google_code_assist.retrieve_user_quota"):
        cli._handle_gquota_command("/gquota")

    assert live_console.print.call_count == 2
    cli.console.print.assert_not_called()
