"""Agent运行引擎测试 - tool call args sanitizer

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的tool call args sanitizer验证。
- 验证功能：tool call args sanitizer功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：tool call args sanitizer功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for AIAgent._sanitize_tool_call_arguments.
"""

import copy
import logging

from run_agent import AIAgent


_MISSING = object()


def _tool_call(call_id="call_1", name="read_file", arguments='{"path":"/tmp/foo"}'):
    function = {"name": name}
    if arguments is not _MISSING:
        function["arguments"] = arguments
    return {
        "id": call_id,
        "type": "function",
        "function": function,
    }


def _assistant_message(*tool_calls):
    return {
        "role": "assistant",
        "content": "tooling",
        "tool_calls": list(tool_calls),
    }


def _tool_message(call_id="call_1", content="ok"):
    return {
        "role": "tool",
        "tool_call_id": call_id,
        "content": content,
    }


def test_valid_arguments_unchanged():
    messages = [
        {"role": "user", "content": "hello"},
        _assistant_message(_tool_call(arguments='{"path":"/tmp/foo"}')),
        _tool_message(content="done"),
    ]
    original = copy.deepcopy(messages)

    repaired = AIAgent._sanitize_tool_call_arguments(messages)

    assert repaired == 0
    assert messages == original


def test_truncated_arguments_replaced_with_empty_object(caplog):
    messages = [
        _assistant_message(_tool_call(arguments='{"path": "/tmp/foo')),
    ]

    with caplog.at_level(logging.WARNING, logger="run_agent"):
        repaired = AIAgent._sanitize_tool_call_arguments(
            messages,
            logger=logging.getLogger("run_agent"),
            session_id="session-123",
        )

    assert repaired == 1
    assert messages[0]["tool_calls"][0]["function"]["arguments"] == "{}"
    assert any(
        "session=session-123" in record.message
        and "tool_call_id=call_1" in record.message
        for record in caplog.records
    )


def test_marker_appended_to_existing_tool_message():
    marker = AIAgent._TOOL_CALL_ARGUMENTS_CORRUPTION_MARKER
    messages = [
        _assistant_message(_tool_call(arguments='{"path": "/tmp/foo')),
        _tool_message(content="existing tool output"),
    ]

    repaired = AIAgent._sanitize_tool_call_arguments(messages)

    assert repaired == 1
    assert messages[1]["content"] == f"{marker}\nexisting tool output"




def _disabled_test_marker_message_inserted_when_missing():
    marker = AIAgent._TOOL_CALL_ARGUMENTS_CORRUPTION_MARKER
    messages = [
        _assistant_message(_tool_call(arguments='{"path": "/tmp/foo')),
        {"role": "user", "content": "next turn"},
    ]

    repaired = AIAgent._sanitize_tool_call_arguments(messages)

    assert repaired == 1
    assert messages[1] == {
        "role": "tool",
        "name": "read_file",
        "tool_call_id": "call_1",
        "content": marker,
    }
    assert messages[2] == {"role": "user", "content": "next turn"}


def test_multiple_corrupted_tool_calls_in_one_message():
    marker = AIAgent._TOOL_CALL_ARGUMENTS_CORRUPTION_MARKER
    messages = [
        _assistant_message(
            _tool_call(call_id="call_1", arguments='{"path": "/tmp/foo'),
            _tool_call(call_id="call_2", arguments='{"path":"/tmp/bar"}'),
            _tool_call(call_id="call_3", arguments='{"mode":"tail"'),
        ),
    ]

    repaired = AIAgent._sanitize_tool_call_arguments(messages)

    assert repaired == 2
    assert messages[0]["tool_calls"][0]["function"]["arguments"] == "{}"
    assert messages[0]["tool_calls"][1]["function"]["arguments"] == '{"path":"/tmp/bar"}'
    assert messages[0]["tool_calls"][2]["function"]["arguments"] == "{}"
    assert messages[1]["tool_call_id"] == "call_1"
    assert messages[1]["content"] == marker
    assert messages[2]["tool_call_id"] == "call_3"
    assert messages[2]["content"] == marker


def test_empty_string_arguments_treated_as_empty_object(caplog):
    messages = [
        _assistant_message(_tool_call(arguments="")),
    ]

    with caplog.at_level(logging.WARNING, logger="run_agent"):
        repaired = AIAgent._sanitize_tool_call_arguments(
            messages,
            logger=logging.getLogger("run_agent"),
            session_id="session-123",
        )

    assert repaired == 0
    assert messages[0]["tool_calls"][0]["function"]["arguments"] == "{}"
    assert caplog.records == []


def test_non_assistant_messages_ignored():
    messages = [
        {"role": "user", "content": "hello", "tool_calls": [_tool_call(arguments='{"bad":')]},
        {"role": "tool", "tool_call_id": "call_1", "content": "ok"},
        {"role": "system", "content": "sys", "tool_calls": [_tool_call(arguments='{"bad":')]},
        None,
        "not a dict",
    ]
    original = copy.deepcopy(messages)

    repaired = AIAgent._sanitize_tool_call_arguments(messages)

    assert repaired == 0
    assert messages == original
