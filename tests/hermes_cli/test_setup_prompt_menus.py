"""命令行界面测试 - 设置·提示词处理·menus

【产品经理理解要点】
验证命令行界面的设置提示词处理功能
- 验证的功能: 初始化提示词菜单交互
- 核心测试场景: prompt strips bracketed paste markers、password prompt strips bracketed paste markers、prompt choice uses curses helper 等共5个场景
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - 初始化设置·提示词处理·menus

测试CLI命令处理与配置管理中setup相关的prompt相关的menus功能
"""

from hermes_cli import setup as setup_mod


def test_prompt_strips_bracketed_paste_markers(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": "\x1b[200~sk-ant-api-key\x1b[201~",
    )

    value = setup_mod.prompt("API key")

    assert value == "sk-ant-api-key"


def test_password_prompt_strips_bracketed_paste_markers(monkeypatch):
    monkeypatch.setattr(
        "getpass.getpass",
        lambda _prompt="": "\x1b[200~secret-token\x1b[201~",
    )

    value = setup_mod.prompt("API key", password=True)

    assert value == "secret-token"


def test_prompt_choice_uses_curses_helper(monkeypatch):
    monkeypatch.setattr(setup_mod, "_curses_prompt_choice", lambda question, choices, default=0, description=None: 1)

    idx = setup_mod.prompt_choice("Pick one", ["a", "b", "c"], default=0)

    assert idx == 1


def test_prompt_choice_falls_back_to_numbered_input(monkeypatch):
    monkeypatch.setattr(setup_mod, "_curses_prompt_choice", lambda question, choices, default=0, description=None: -1)
    monkeypatch.setattr("builtins.input", lambda _prompt="": "2")

    idx = setup_mod.prompt_choice("Pick one", ["a", "b", "c"], default=0)

    assert idx == 1


def test_prompt_checklist_uses_shared_curses_checklist(monkeypatch):
    monkeypatch.setattr(
        "hermes_cli.curses_ui.curses_checklist",
        lambda title, items, selected, cancel_returns=None: {0, 2},
    )

    selected = setup_mod.prompt_checklist("Pick tools", ["one", "two", "three"], pre_selected=[1])

    assert selected == [0, 2]
