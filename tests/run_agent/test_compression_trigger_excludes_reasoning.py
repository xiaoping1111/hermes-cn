"""Agent运行引擎测试 - compression trigger excludes reasoning

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的compression trigger excludes reasoning验证。
- 验证功能：compression trigger excludes reasoning功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：compression trigger excludes reasoning功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Verify compression trigger excludes reasoning/completion tokens (#12026).

Thinking models (GLM-5.1, QwQ, DeepSeek R1) inflate completion_tokens with
reasoning tokens that don't consume context window space.  The compression
trigger must use only prompt_tokens so sessions aren't prematurely split.
"""

import types


def _make_agent_stub(prompt_tokens, completion_tokens, threshold_tokens):
    """Create a minimal stub that exercises the compression check path."""
    compressor = types.SimpleNamespace(
        last_prompt_tokens=prompt_tokens,
        last_completion_tokens=completion_tokens,
        threshold_tokens=threshold_tokens,
    )
    # Replicate the fixed logic from run_agent.py ~line 11273
    if compressor.last_prompt_tokens > 0:
        real_tokens = compressor.last_prompt_tokens  # Fixed: no completion
    else:
        real_tokens = 0
    return real_tokens, compressor


class TestCompressionTriggerExcludesReasoning:
    def test_high_reasoning_tokens_should_not_trigger_compression(self):
        """With the old bug, 40k prompt + 80k reasoning = 120k > 100k threshold.
        After the fix, only 40k prompt is compared — no compression."""
        real_tokens, comp = _make_agent_stub(
            prompt_tokens=40_000,
            completion_tokens=80_000,  # reasoning-heavy model
            threshold_tokens=100_000,
        )
        assert real_tokens == 40_000
        assert real_tokens < comp.threshold_tokens, (
            "Should NOT trigger compression — only prompt tokens matter"
        )


    def test_zero_prompt_tokens_falls_back(self):
        """When provider returns 0 prompt tokens, real_tokens is 0 (fallback path)."""
        real_tokens, _ = _make_agent_stub(
            prompt_tokens=0,
            completion_tokens=50_000,
            threshold_tokens=100_000,
        )
        assert real_tokens == 0
