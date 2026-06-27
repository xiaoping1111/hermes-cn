"""Agent运行引擎测试 - redirect stdout issue

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的redirect stdout issue验证。
- 验证功能：redirect stdout issue功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：redirect stdout issue功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Verify that redirect_stdout in _run_single_child is process-wide.

This demonstrates that contextlib.redirect_stdout changes sys.stdout
for ALL threads, not just the current one. This means during subagent
execution, all output from other threads (including the CLI's process_thread)
is swallowed.
"""

import contextlib
import io
import sys
import threading
import time
import unittest


class TestRedirectStdoutIsProcessWide(unittest.TestCase):

    def test_redirect_stdout_affects_other_threads(self):
        """contextlib.redirect_stdout changes sys.stdout for ALL threads."""
        captured_from_other_thread = []
        real_stdout = sys.stdout
        other_thread_saw_devnull = threading.Event()

        def other_thread_work():
            """Runs in a different thread, tries to use sys.stdout."""
            time.sleep(0.2)  # Let redirect_stdout take effect
            # Check what sys.stdout is
            if sys.stdout is not real_stdout:
                other_thread_saw_devnull.set()
            # Try to print — this should go to devnull
            captured_from_other_thread.append(sys.stdout)

        t = threading.Thread(target=other_thread_work, daemon=True)
        t.start()

        # redirect_stdout in main thread
        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull):
            time.sleep(0.5)  # Let the other thread check during redirect

        t.join(timeout=2)

        # The other thread should have seen devnull, NOT the real stdout
        self.assertTrue(
            other_thread_saw_devnull.is_set(),
            "redirect_stdout was NOT process-wide — other thread still saw real stdout. "
            "This test's premise is wrong."
        )
        print("Confirmed: redirect_stdout IS process-wide — affects all threads")


if __name__ == "__main__":
    unittest.main()
