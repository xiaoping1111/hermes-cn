import psutil
"""测试 - slash worker watchdog

【产品经理理解要点】
功能验证中的slash worker watchdog验证。
- 验证功能：slash worker watchdog功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：slash worker watchdog功能异常或存在安全隐患"""


from tui_gateway import slash_worker


def test_is_orphaned_true_when_ppid_changes():
    # Our parent went away and we were reparented to a subreaper/init.
    assert slash_worker._is_orphaned(1234, 1.0, getppid=lambda: 999999) is True


def test_is_orphaned_true_when_parent_create_time_mismatch():
    # Same ppid but a different create_time means the PID was reused.
    me = psutil.Process()
    assert slash_worker._is_orphaned(me.pid, 0.0, getppid=lambda: me.pid) is True


def test_is_orphaned_false_when_parent_alive_and_matches():
    me = psutil.Process()
    assert (
        slash_worker._is_orphaned(me.pid, me.create_time(), getppid=lambda: me.pid) is False
    )
