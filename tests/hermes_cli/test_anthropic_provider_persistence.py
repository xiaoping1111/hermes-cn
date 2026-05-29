"""命令行界面测试 - anthropic·提供商·持久化

【产品经理理解要点】
验证命令行界面的提供商持久化功能
- 验证的功能: Tests for Anthropic credential persistence helpers
- 核心测试场景: save anthropic oauth token uses token slot and clears api key、use anthropic claude code credentials clears env slots、save anthropic api key uses api key slot and clears token
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Tests for Anthropic credential persistence helpers.
"""

from hermes_cli.config import load_env


def test_save_anthropic_oauth_token_uses_token_slot_and_clears_api_key(tmp_path, monkeypatch):
    home = tmp_path / "hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))

    from hermes_cli.config import save_anthropic_oauth_token

    save_anthropic_oauth_token("sk-ant-oat01-test-token")

    env_vars = load_env()
    assert env_vars["ANTHROPIC_TOKEN"] == "sk-ant-oat01-test-token"
    assert env_vars["ANTHROPIC_API_KEY"] == ""


def test_use_anthropic_claude_code_credentials_clears_env_slots(tmp_path, monkeypatch):
    home = tmp_path / "hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))

    from hermes_cli.config import save_anthropic_oauth_token, use_anthropic_claude_code_credentials

    save_anthropic_oauth_token("sk-ant-oat01-token")
    use_anthropic_claude_code_credentials()

    env_vars = load_env()
    assert env_vars["ANTHROPIC_TOKEN"] == ""
    assert env_vars["ANTHROPIC_API_KEY"] == ""


def test_save_anthropic_api_key_uses_api_key_slot_and_clears_token(tmp_path, monkeypatch):
    home = tmp_path / "hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))

    from hermes_cli.config import save_anthropic_api_key

    save_anthropic_api_key("sk-ant-api03-key")

    env_vars = load_env()
    assert env_vars["ANTHROPIC_API_KEY"] == "sk-ant-api03-key"
    assert env_vars["ANTHROPIC_TOKEN"] == ""
