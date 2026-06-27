"""CLIanthropic oauth flow测试

【产品经理理解要点】
CLIanthropic oauth flow功能测试。
- 验证功能：命令行anthropic oauth flow功能
- 关键场景：配置、执行、验证
- 业务影响：anthropic oauth flow命令行功能失效

─────────────────────────────────────────────────────────────────────────
Tests for Anthropic OAuth setup flow behavior."""

from hermes_cli.config import load_env, save_env_value


def test_run_anthropic_oauth_flow_prefers_claude_code_credentials(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setattr(
        "agent.anthropic_adapter.run_oauth_setup_token",
        lambda: "sk-ant-oat01-from-claude-setup",
    )
    monkeypatch.setattr(
        "agent.anthropic_adapter.read_claude_code_credentials",
        lambda: {
            "accessToken": "cc-access-token",
            "refreshToken": "cc-refresh-token",
            "expiresAt": 9999999999999,
        },
    )
    monkeypatch.setattr(
        "agent.anthropic_adapter.is_claude_code_token_valid",
        lambda creds: True,
    )

    from hermes_cli.main import _run_anthropic_oauth_flow

    save_env_value("ANTHROPIC_TOKEN", "stale-env-token")
    assert _run_anthropic_oauth_flow(save_env_value) is True

    env_vars = load_env()
    assert env_vars["ANTHROPIC_TOKEN"] == ""
    assert env_vars["ANTHROPIC_API_KEY"] == ""
    output = capsys.readouterr().out
    assert "Claude Code credentials linked" in output


def test_run_anthropic_oauth_flow_manual_token_still_persists(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setattr("agent.anthropic_adapter.run_oauth_setup_token", lambda: None)
    monkeypatch.setattr("agent.anthropic_adapter.read_claude_code_credentials", lambda: None)
    monkeypatch.setattr("agent.anthropic_adapter.is_claude_code_token_valid", lambda creds: False)
    monkeypatch.setattr("builtins.input", lambda _prompt="": "sk-ant-oat01-manual-token")
    monkeypatch.setattr(
        "hermes_cli.secret_prompt.masked_secret_prompt",
        lambda _prompt="": "sk-ant-oat01-manual-token",
    )

    from hermes_cli.main import _run_anthropic_oauth_flow

    assert _run_anthropic_oauth_flow(save_env_value) is True

    env_vars = load_env()
    assert env_vars["ANTHROPIC_TOKEN"] == "sk-ant-oat01-manual-token"
    output = capsys.readouterr().out
    assert "Setup-token saved" in output
