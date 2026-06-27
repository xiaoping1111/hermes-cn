"""CLIwindows native docs测试

【产品经理理解要点】
CLIwindows native docs功能测试。
- 验证功能：命令行windows native docs功能
- 关键场景：配置、执行、验证
- 业务影响：windows native docs命令行功能失效"""

from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\hermes\\hermes-agent\\venv\\Scripts" in doc
    assert "Get-Command hermes        # should print C:\\Users\\<you>\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\hermes.exe" in doc
    assert '$hermesBin = "$InstallDir\\venv\\Scripts"' in install
