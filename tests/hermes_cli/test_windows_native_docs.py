"""【产品经理理解要点】
CLI模块测试——验证命令行各子模块（test_windows_native_docs.py）
"""

from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\hermes\\hermes-agent\\venv\\Scripts" in doc
    assert "Get-Command hermes        # should print C:\\Users\\<you>\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\hermes.exe" in doc
    assert '$hermesBin = "$InstallDir\\venv\\Scripts"' in install
