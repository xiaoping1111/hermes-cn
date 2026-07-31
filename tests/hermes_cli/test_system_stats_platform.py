"""CLIsystem stats platform测试

【产品经理理解要点】
CLIsystem stats platform功能测试。
- 验证功能：命令行system stats platform功能
- 关键场景：配置、执行、验证
- 业务影响：system stats platform命令行功能失效"""

from hermes_cli.web_server import _display_system_platform


def test_windows_11_build_displays_as_windows_11():
    info = _display_system_platform(
        system="Windows",
        release="10",
        version="10.0.26200",
        platform_label="Windows-10-10.0.26200-SP0",
    )

    assert info["os"] == "Windows"
    assert info["os_release"] == "11"
    assert info["os_version"] == "10.0.26200"
    assert info["platform"] == "Windows-11-10.0.26200-SP0"


def test_non_windows_platform_unchanged():
    info = _display_system_platform(
        system="Linux",
        release="6.8.0",
        version="#1 SMP",
        platform_label="Linux-6.8.0-x86_64-with-glibc2.39",
    )

    assert info == {
        "os": "Linux",
        "os_release": "6.8.0",
        "os_version": "#1 SMP",
        "platform": "Linux-6.8.0-x86_64-with-glibc2.39",
    }
