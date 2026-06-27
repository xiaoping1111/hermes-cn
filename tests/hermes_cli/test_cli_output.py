"""CLIcli output测试

【产品经理理解要点】
CLIcli output功能测试。
- 验证功能：命令行cli output功能
- 关键场景：配置、执行、验证
- 业务影响：cli output命令行功能失效"""

from hermes_cli import cli_output


def test_password_prompt_uses_masked_secret_prompt(monkeypatch):
    seen = {}

    def fake_masked_secret_prompt(display):
        seen["display"] = display
        return " secret "

    monkeypatch.setattr(cli_output, "masked_secret_prompt", fake_masked_secret_prompt)

    assert cli_output.prompt("API key", default="old", password=True) == "secret"
    assert "API key [old]" in seen["display"]


def test_empty_password_prompt_returns_default(monkeypatch):
    monkeypatch.setattr(cli_output, "masked_secret_prompt", lambda _display: "")

    assert cli_output.prompt("API key", default="old", password=True) == "old"
