"""命令行界面测试 - banner·pip·更新

【产品经理理解要点】
验证命令行界面的更新功能
- 验证的功能: 启动横幅pip更新检测
- 核心测试场景: version tuple comparison
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - banner·pip·配置更新

测试CLI命令处理与配置管理中banner相关的pip相关的update功能
"""

from unittest.mock import patch


def testcheck_via_pypi_detects_update():
    """check_via_pypi returns 1 when PyPI has newer version."""
    from hermes_cli.banner import check_via_pypi
    with patch("hermes_cli.banner.VERSION", "0.12.0"):
        with patch("hermes_cli.banner._fetch_pypi_latest", return_value="0.13.0"):
            result = check_via_pypi()
            assert result == 1


def testcheck_via_pypi_up_to_date():
    """check_via_pypi returns 0 when versions match."""
    from hermes_cli.banner import check_via_pypi
    with patch("hermes_cli.banner.VERSION", "0.13.0"):
        with patch("hermes_cli.banner._fetch_pypi_latest", return_value="0.13.0"):
            result = check_via_pypi()
            assert result == 0


def testcheck_via_pypi_network_failure():
    """check_via_pypi returns None on network error."""
    from hermes_cli.banner import check_via_pypi
    with patch("hermes_cli.banner._fetch_pypi_latest", return_value=None):
        result = check_via_pypi()
        assert result is None


def test_version_tuple_comparison():
    """Version comparison works with multi-segment versions."""
    from hermes_cli.banner import _version_tuple
    assert _version_tuple("0.13.0") > _version_tuple("0.12.0")
    assert _version_tuple("0.13.0") == _version_tuple("0.13.0")
    assert _version_tuple("1.0.0") > _version_tuple("0.99.99")
