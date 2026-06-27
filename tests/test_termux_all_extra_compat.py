"""测试 - termux all extra compat

【产品经理理解要点】
功能验证中的termux all extra compat验证。
- 验证功能：termux all extra compat功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：termux all extra compat功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression coverage for the Termux broad install profile.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"
INSTALL_SH = REPO_ROOT / "scripts" / "install.sh"


def test_pyproject_defines_termux_all_without_known_blockers() -> None:
    text = PYPROJECT.read_text()
    assert "termux-all = [" in text
    assert '"hermes-agent[termux]"' in text
    assert '"hermes-agent[matrix]"' not in text.split("termux-all = [", 1)[1].split("]", 1)[0]
    assert '"hermes-agent[voice]"' not in text.split("termux-all = [", 1)[1].split("]", 1)[0]


def test_install_script_prefers_termux_all_then_fallbacks() -> None:
    text = INSTALL_SH.read_text()
    assert "pip install -e '.[termux-all]' -c constraints-termux.txt" in text
    assert "Termux broad profile (.[termux-all]) failed, trying baseline Termux profile..." in text
    assert "Termux baseline profile (.[termux]) failed, trying base install..." in text
