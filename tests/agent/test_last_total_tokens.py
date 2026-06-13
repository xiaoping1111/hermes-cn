"""Test that last_total_tokens is correctly set by ContextCompressor.

【产品经理理解要点】
代理核心测试——验证对话引擎、模型适配、上下文压缩等（test_last_total_tokens.py）
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
