from __future__ import annotations
"""Agent核心测试 - direct provider url detection

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的direct provider url detection验证。
- 验证功能：direct provider url detection功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：direct provider url detection功能异常或存在安全隐患"""


from run_agent import AIAgent


def _agent_with_base_url(base_url: str) -> AIAgent:
    agent = object.__new__(AIAgent)
    agent.base_url = base_url
    return agent


def test_direct_openai_url_requires_openai_host():
    agent = _agent_with_base_url("https://api.openai.com.example/v1")

    assert agent._is_direct_openai_url() is False




def test_direct_openai_url_accepts_native_host():
    agent = _agent_with_base_url("https://api.openai.com/v1")

    assert agent._is_direct_openai_url() is True
