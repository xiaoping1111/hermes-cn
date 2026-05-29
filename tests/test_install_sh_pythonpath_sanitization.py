"""安装脚本Python路径清理测试

【产品经理理解要点】
验证安装脚本清理继承的PYTHONPATH/PYTHONHOME，防止其他Python环境干扰安装。
- 安装时取消PYTHONPATH和PYTHONHOME
- 运行时启动器也清理这些变量
- 影响从其他Python工具链安装的兼容性

──────────────────────────────────────────────────────────────
Regression tests for install.sh Python environment sanitization.

When install.sh is launched from another Python-driven tool session, inherited
PYTHONPATH/PYTHONHOME can shadow the freshly installed checkout. The installer
must sanitize those vars both during installation and at runtime launch.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SH = REPO_ROOT / "scripts" / "install.sh"


def test_install_script_unsets_pythonpath_and_pythonhome_early() -> None:
    text = INSTALL_SH.read_text()

    # During install, inherited Python env must be sanitized before pip/venv use.
    assert 'unset PYTHONPATH' in text
    assert 'unset PYTHONHOME' in text


def test_hermes_launcher_wrapper_clears_python_env_before_exec() -> None:
    text = INSTALL_SH.read_text()

    # Wrapper should clear env and forward args untouched to the venv entrypoint.
    assert 'cat > "$command_link_dir/hermes" <<EOF' in text
    assert 'unset PYTHONPATH' in text
    assert 'unset PYTHONHOME' in text
    assert 'exec "$HERMES_BIN" "\\$@"' in text
