"""CLIsetup prompt menus测试

【产品经理理解要点】
CLIsetup prompt menus功能测试。
- 验证功能：命令行setup prompt menus功能
- 关键场景：配置、执行、验证
- 业务影响：setup prompt menus命令行功能失效"""

from hermes_cli import setup as setup_mod


def test_prompt_strips_bracketed_paste_markers(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": "\x1b[200~sk-ant-api-key\x1b[201~",
    )

    value = setup_mod.prompt("API key")

    assert value == "sk-ant-api-key"




def test_prompt_choice_uses_curses_helper(monkeypatch):
    monkeypatch.setattr(setup_mod, "_curses_prompt_choice", lambda question, choices, default=0, description=None: 1)

    idx = setup_mod.prompt_choice("Pick one", ["a", "b", "c"], default=0)

    assert idx == 1


