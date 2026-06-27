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

from agent.tool_result_classification import file_mutation_result_landed


def test_write_file_with_nested_lint_error_counts_as_landed():
    result = json.dumps({
        "bytes_written": 12,
        "lint": {"status": "error", "output": "SyntaxError: invalid syntax"},
    })

    assert file_mutation_result_landed("write_file", result) is True


def test_patch_with_nested_lsp_diagnostics_counts_as_landed():
    result = json.dumps({
        "success": True,
        "diff": "--- a/tmp.py\n+++ b/tmp.py\n",
        "lsp_diagnostics": "<diagnostics>ERROR [1:1] type mismatch</diagnostics>",
    })

    assert file_mutation_result_landed("patch", result) is True


def test_top_level_file_mutation_error_does_not_count_as_landed():
    result = json.dumps({"success": True, "error": "post-write verification failed"})

    assert file_mutation_result_landed("patch", result) is False
