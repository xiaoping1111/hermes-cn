"""Agent核心测试 - tool result classification

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的tool result classification验证。
- 验证功能：tool result classification功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：tool result classification功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for shared tool result classification helpers.
"""

import json

from agent.tool_result_classification import (
    file_mutation_result_landed,
)


def test_write_file_with_nested_lint_error_counts_as_landed():
    result = json.dumps({
        "bytes_written": 12,
        "lint": {"status": "error", "output": "SyntaxError: invalid syntax"},
    })

    assert file_mutation_result_landed("write_file", result) is True






def test_side_effect_classification_keeps_session_mutations():
    from agent.tool_result_classification import tool_may_have_side_effect

    assert tool_may_have_side_effect("todo") is True
    assert tool_may_have_side_effect("memory") is True
    assert tool_may_have_side_effect("write_file") is True
    assert tool_may_have_side_effect("mcp_unknown") is True
    assert tool_may_have_side_effect("read_file") is False
    assert tool_may_have_side_effect("web_search") is False
