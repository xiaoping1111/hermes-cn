"""命令行界面测试 - reasoning·effort·menu

【产品经理理解要点】
验证命令行界面相关功能的正确性
- 验证的功能: 推理深度菜单配置
- 核心测试场景: reasoning menu orders minimal before low
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - reasoning·effort·menu

测试CLI命令处理与配置管理中reasoning相关的effort相关的menu功能
"""

import sys
import types


from hermes_cli.main import _prompt_reasoning_effort_selection


class _FakeTerminalMenu:
    last_choices = None

    def __init__(self, choices, **kwargs):
        _FakeTerminalMenu.last_choices = choices
        self._cursor_index = kwargs.get("cursor_index")

    def show(self):
        return self._cursor_index


def test_reasoning_menu_orders_minimal_before_low(monkeypatch):
    fake_module = types.SimpleNamespace(TerminalMenu=_FakeTerminalMenu)
    monkeypatch.setitem(sys.modules, "simple_term_menu", fake_module)

    selected = _prompt_reasoning_effort_selection(
        ["low", "minimal", "medium", "high"],
        current_effort="medium",
    )

    assert selected == "medium"
    assert _FakeTerminalMenu.last_choices[:4] == [
        "  minimal",
        "  low",
        "  medium  ← currently in use",
        "  high",
    ]
