"""CLIrun with idle timeout测试

【产品经理理解要点】
CLIrun with idle timeout功能测试。
- 验证功能：命令行run with idle timeout功能
- 关键场景：配置、执行、验证
- 业务影响：run with idle timeout命令行功能失效

─────────────────────────────────────────────────────────────────────────
Coverage for _run_with_idle_timeout — the streaming subprocess helper.

Kept in a dedicated test file because the tests spawn real ``subprocess.Popen``
instances; pytest-isolate runs each test file in its own worker process, so
isolating these here prevents real-Popen state from racing with the
``subprocess.run`` / ``_run_with_idle_timeout`` patches used by
``test_web_ui_build.py``.

Added for issue #33788: ``hermes update`` got stuck at "webui-build" because
``npm run build`` ran with ``capture_output=True`` and no timeout. The helper
fixes both halves — streams output AND idle-kills the process."""

import sys as _sys
import time

from hermes_cli.main import _run_with_idle_timeout


def test_streams_output_and_returns_zero_on_success(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('line one'); print('line two')\n")
    result = _run_with_idle_timeout(
        [_sys.executable, str(script)], cwd=tmp_path, idle_timeout_seconds=10
    )
    assert result.returncode == 0
    assert "line one" in result.stdout
    assert "line two" in result.stdout


def test_returns_127_when_binary_missing(tmp_path):
    result = _run_with_idle_timeout(
        ["/nonexistent/binary/does/not/exist"],
        cwd=tmp_path,
        idle_timeout_seconds=5,
    )
    assert result.returncode == 127
