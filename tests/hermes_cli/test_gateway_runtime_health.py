"""命令行界面测试 - gateway·runtime·健康检查

【产品经理理解要点】
验证命令行界面的健康检查功能
- 验证的功能: 网关运行时健康检查
- 核心测试场景: runtime health lines include fatal platform and startup reason
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - gateway·runtime·健康检查

测试CLI命令处理与配置管理中gateway相关的runtime相关的health功能
"""

from hermes_cli.gateway import _runtime_health_lines


def test_runtime_health_lines_include_fatal_platform_and_startup_reason(monkeypatch):
    monkeypatch.setattr(
        "gateway.status.read_runtime_status",
        lambda: {
            "gateway_state": "startup_failed",
            "exit_reason": "telegram conflict",
            "platforms": {
                "telegram": {
                    "state": "fatal",
                    "error_message": "another poller is active",
                }
            },
        },
    )

    lines = _runtime_health_lines()

    assert "⚠ telegram: another poller is active" in lines
    assert "⚠ Last startup issue: telegram conflict" in lines
