"""命令行界面测试 - 设置·hermes·脚本执行

【产品经理理解要点】
验证命令行界面的设置脚本执行功能
- 验证的功能: Hermes安装脚本执行
- 核心测试场景: setup hermes script is valid shell、setup hermes script has termux path
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - 初始化设置·hermes·脚本执行

测试CLI命令处理与配置管理中setup相关的hermes相关的script功能
"""

from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[2]
SETUP_SCRIPT = REPO_ROOT / "setup-hermes.sh"


def test_setup_hermes_script_is_valid_shell():
    result = subprocess.run(["bash", "-n", str(SETUP_SCRIPT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_setup_hermes_script_has_termux_path():
    content = SETUP_SCRIPT.read_text(encoding="utf-8")

    assert "is_termux()" in content
    assert ".[termux]" in content
    assert "constraints-termux.txt" in content
    assert "$PREFIX/bin" in content
