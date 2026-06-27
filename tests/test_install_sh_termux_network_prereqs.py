"""测试 - install sh termux network prereqs

【产品经理理解要点】
功能验证中的install sh termux network prereqs验证。
- 验证功能：install sh termux network prereqs功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：install sh termux network prereqs功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for Termux network prerequisite handling in install.sh.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SH = REPO_ROOT / "scripts" / "install.sh"


def test_termux_pkg_list_includes_network_basics() -> None:
    text = INSTALL_SH.read_text()
    assert "local termux_pkgs=(clang rust make pkg-config libffi openssl ca-certificates curl)" in text


def test_install_script_has_connectivity_probe_and_termux_guidance() -> None:
    text = INSTALL_SH.read_text()
    assert "check_network_prerequisites()" in text
    assert "https://pypi.org/simple/" in text
    assert "https://duckduckgo.com/" in text
    assert "termux-change-repo" in text
    assert "pkg install -y ca-certificates curl && pkg update" in text
    assert "check_network_prerequisites" in text
