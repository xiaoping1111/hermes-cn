"""CLI终端测试 - cli bracketed paste sanitizer

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的cli bracketed paste sanitizer验证。
- 验证功能：cli bracketed paste sanitizer功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：cli bracketed paste sanitizer功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for defensive bracketed-paste wrapper stripping in the CLI.
"""

from cli import _strip_leaked_bracketed_paste_wrappers


class TestStripLeakedBracketedPasteWrappers:

    def test_strips_canonical_escape_wrappers(self):
        text = "\x1b[200~hello\x1b[201~"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "hello"

    def test_strips_visible_caret_escape_wrappers(self):
        text = "^[[200~hello^[[201~"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "hello"


    def test_strips_degraded_bracket_only_wrappers_after_whitespace(self):
        text = "prefix [200~hello[201~ suffix"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "prefix hello suffix"


    def test_strips_wrapper_fragments_after_whitespace(self):
        text = "prefix 00~hello world01~ suffix"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "prefix hello world suffix"



    def test_preserves_multiline_content_while_stripping_wrappers(self):
        text = "^[[200~line 1\nline 2\nline 3^[[201~"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "line 1\nline 2\nline 3"

    def test_preserves_multiline_content_while_stripping_degraded_bracket_only_wrappers(self):
        text = "[200~line 1\nline 2\nline 3[201~"
        assert _strip_leaked_bracketed_paste_wrappers(text) == "line 1\nline 2\nline 3"
