"""CLI终端测试 - prepend note to message

【产品经理理解要点】
命令行交互界面：斜杠命令、会话管理、压缩、编辑器、状态栏、快捷键等用户体验中的prepend note to message验证。
- 验证功能：prepend note to message功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：prepend note to message功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for cli._prepend_note_to_message.

Regression coverage for the TypeError raised when a queued /model or
/reload-skills note was prepended to a multimodal (image-attached) message:
``can only concatenate str (not "list") to str``.
"""

from cli import _prepend_note_to_message


def test_string_message_gets_note_prepended():
    assert _prepend_note_to_message("hello", "NOTE") == "NOTE\n\nhello"




def test_note_is_stripped():
    assert _prepend_note_to_message("hello", "  NOTE  ") == "NOTE\n\nhello"






def test_list_message_folds_note_into_first_text_part():
    message = [
        {"type": "text", "text": "describe this"},
        {"type": "image_url", "image_url": {"url": "data:..."}},
    ]
    result = _prepend_note_to_message(message, "NOTE")

    assert result[0]["type"] == "text"
    assert result[0]["text"] == "NOTE\n\ndescribe this"
    # Image part is preserved untouched.
    assert result[1] == {"type": "image_url", "image_url": {"url": "data:..."}}
    # Original message is not mutated.
    assert message[0]["text"] == "describe this"


def test_image_only_list_gets_leading_text_part():
    message = [{"type": "image_url", "image_url": {"url": "data:..."}}]
    result = _prepend_note_to_message(message, "NOTE")

    assert result[0] == {"type": "text", "text": "NOTE"}
    assert result[1]["type"] == "image_url"




def test_unknown_shape_returned_unchanged():
    assert _prepend_note_to_message(123, "NOTE") == 123
    assert _prepend_note_to_message(None, "NOTE") is None
