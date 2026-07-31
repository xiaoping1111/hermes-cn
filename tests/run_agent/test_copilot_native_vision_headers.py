from unittest.mock import MagicMock, patch
"""Agent运行引擎测试 - copilot native vision headers

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的copilot native vision headers验证。
- 验证功能：copilot native vision headers功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：copilot native vision headers功能异常或存在安全隐患"""


from run_agent import AIAgent


def _make_copilot_agent():
    with patch("run_agent.OpenAI") as mock_openai:
        mock_openai.return_value = MagicMock()
        agent = AIAgent(
            api_key="gh-token",
            base_url="https://api.githubcopilot.com",
            provider="copilot",
            model="gpt-5.4",
            quiet_mode=True,
            skip_context_files=True,
            skip_memory=True,
        )
    return agent


def test_request_client_adds_copilot_vision_header_for_native_image_payload():
    agent = _make_copilot_agent()
    built_kwargs = []

    def fake_create(kwargs, *, reason, shared):
        built_kwargs.append(dict(kwargs))
        return MagicMock()

    api_kwargs = {
        "model": "gpt-5.4",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64,abc"}},
                ],
            }
        ],
    }

    agent.client = object()
    with patch.object(agent, "_is_openai_client_closed", return_value=False), patch.object(
        agent, "_create_openai_client", side_effect=fake_create
    ):
        agent._create_request_openai_client(reason="test", api_kwargs=api_kwargs)

    headers = built_kwargs[-1]["default_headers"]
    assert headers["Copilot-Vision-Request"] == "true"




