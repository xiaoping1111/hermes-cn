"""CLIanthropic provider persistence测试

【产品经理理解要点】
CLIanthropic provider persistence功能测试。
- 验证功能：命令行anthropic provider persistence功能
- 关键场景：配置、执行、验证
- 业务影响：anthropic provider persistence命令行功能失效

─────────────────────────────────────────────────────────────────────────
Tests for Anthropic credential persistence helpers."""

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


