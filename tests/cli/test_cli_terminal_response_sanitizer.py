"""CLI终端测试 - cli terminal response sanitizer

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的cli terminal response sanitizer验证。
- 验证功能：cli terminal response sanitizer功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：cli terminal response sanitizer功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for defensive terminal control-response stripping in the CLI.

Covers Cursor Position Report (CPR / DSR) responses that occasionally
leak into the input buffer after terminal resize storms or multiplexer
tab switches — see issue #14692.
"""

from cli import _strip_leaked_terminal_responses


class TestStripLeakedTerminalResponses:


    def test_strips_canonical_dsr_response(self):
        # Reports from issue #14692
        text = "\x1b[53;1R"
        assert _strip_leaked_terminal_responses(text) == ""


    def test_strips_multiple_dsr_responses(self):
        text = "a\x1b[53;1Rb\x1b[51;1Rc\x1b[50;9Rd"
        assert _strip_leaked_terminal_responses(text) == "abcd"






    def test_strips_sgr_mouse_report_esc_form(self):
        text = "abc\x1b[<65;1;49Mdef"
        assert _strip_leaked_terminal_responses(text) == "abcdef"



    def test_strips_sgr_mouse_report_with_large_coordinates(self):
        text = "abc\x1b[<10000;12345;98765Mdef"
        assert _strip_leaked_terminal_responses(text) == "abcdef"

    def test_strips_multiple_concatenated_sgr_mouse_reports(self):
        text = "<65;1;49M<35;1;42Mhello<64;1;40m"
        assert _strip_leaked_terminal_responses(text) == "hello"

