"""命令行界面测试 - TUI捆绑模式

【产品经理理解要点】
验证CLI终端UI捆绑模式的正确性
- 验证的功能: TUI捆绑入口JS文件的查找与加载
- 核心测试场景: tui finds bundled entry js、tui returns none when no bundle
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验
"""

from pathlib import Path


def test_tui_finds_bundled_entry_js(tmp_path):
    """_find_bundled_tui finds entry.js bundled in the package."""
    tui_dist = tmp_path / "hermes_cli" / "tui_dist"
    tui_dist.mkdir(parents=True)
    entry = tui_dist / "entry.js"
    entry.write_text("// bundled TUI", encoding="utf-8")

    from hermes_cli.main import _find_bundled_tui
    result = _find_bundled_tui(hermes_cli_dir=tmp_path / "hermes_cli")
    assert result is not None
    assert result.name == "entry.js"


def test_tui_returns_none_when_no_bundle(tmp_path):
    """_find_bundled_tui returns None when no bundle exists."""
    from hermes_cli.main import _find_bundled_tui
    result = _find_bundled_tui(hermes_cli_dir=tmp_path / "hermes_cli")
    assert result is None
