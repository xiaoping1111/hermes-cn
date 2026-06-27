"""Agent核心测试 - last total tokens

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的last total tokens验证。
- 验证功能：last total tokens功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：last total tokens功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Test that last_total_tokens is correctly set by ContextCompressor.
"""

from agent.context_compressor import ContextCompressor


def test_update_from_response_sets_total_tokens():
    """ABC contract: last_total_tokens must be set from API response."""
    c = ContextCompressor(model="test", quiet_mode=True, config_context_length=200000)

    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130})
    assert c.last_total_tokens == 130

    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30})
    assert c.last_total_tokens == 130


def test_session_reset_clears_total_tokens():
    """on_session_reset must zero total_tokens."""
    c = ContextCompressor(model="test", quiet_mode=True, config_context_length=200000)
    c.update_from_response({"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130})
    c.on_session_reset()
    assert c.last_total_tokens == 0
