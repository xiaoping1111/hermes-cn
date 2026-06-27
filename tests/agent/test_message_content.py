from __future__ import annotations
"""Agent核心测试 - message content

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的message content验证。
- 验证功能：message content功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：message content功能异常或存在安全隐患"""


from types import SimpleNamespace

from agent.message_content import flatten_message_text


def test_flatten_message_text_accepts_chat_and_responses_text_parts():
    content = [
        {"type": "text", "text": "chat text"},
        {"type": "input_text", "text": "user text"},
        {"type": "output_text", "text": "assistant text"},
        {"type": "summary_text", "text": "summary text"},
    ]

    assert flatten_message_text(content) == "chat text\nuser text\nassistant text\nsummary text"


def test_flatten_message_text_accepts_object_parts():
    content = [
        SimpleNamespace(type="output_text", text="object text"),
        {"content": "legacy content"},
    ]

    assert flatten_message_text(content) == "object text\nlegacy content"
