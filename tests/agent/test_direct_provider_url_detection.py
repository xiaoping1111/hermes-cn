from __future__ import annotations
"""直连提供商URL检测测试

【产品经理理解要点】
验证用户配置base_url时提供商的正确检测，防止子字符串误匹配。
- 自定义URL的正确提供商识别
- URL子字符串不导致误判
- 影响自定义端点用户的功能可用性
"""


from run_agent import AIAgent


def _agent_with_base_url(base_url: str) -> AIAgent:
    agent = object.__new__(AIAgent)
    agent.base_url = base_url
    return agent


def test_direct_openai_url_requires_openai_host():
    agent = _agent_with_base_url("https://api.openai.com.example/v1")

    assert agent._is_direct_openai_url() is False


def test_direct_openai_url_ignores_path_segment_match():
    agent = _agent_with_base_url("https://proxy.example.test/api.openai.com/v1")

    assert agent._is_direct_openai_url() is False


def test_direct_openai_url_accepts_native_host():
    agent = _agent_with_base_url("https://api.openai.com/v1")

    assert agent._is_direct_openai_url() is True
