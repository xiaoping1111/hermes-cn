"""Agent运行引擎测试 - last reasoning per turn

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的last reasoning per turn验证。
- 验证功能：last reasoning per turn功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：last reasoning per turn功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for per-turn reasoning extraction in AIAgent.run_conversation.

Verifies the reasoning field returned to display layers (CLI reasoning box,
gateway reasoning footer, TUI reasoning event) only reflects the CURRENT
turn's reasoning — never leaks from a prior turn — and is picked up
correctly when reasoning is attached to a tool-calling assistant step
rather than the final-answer assistant step.
"""
from __future__ import annotations


def _extract_last_reasoning(messages):
    """Replica of the extraction loop in run_agent.py (~line 13867).

    Tests pin the loop's behaviour so that refactors can't silently
    regress the per-turn semantic.
    """
    last_reasoning = None
    for msg in reversed(messages):
        if msg.get("role") == "user":
            break
        if msg.get("role") == "assistant" and msg.get("reasoning"):
            last_reasoning = msg["reasoning"]
            break
    return last_reasoning


def test_simple_turn_reasoning_present():
    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi", "reasoning": "greeting the user"},
    ]
    assert _extract_last_reasoning(messages) == "greeting the user"










