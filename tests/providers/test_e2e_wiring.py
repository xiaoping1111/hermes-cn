"""端到端连线测试

【产品经理理解要点】
验证模型提供者模块中nvidia gets default max tokens等6个场景的正确性
- nvidia gets default max tokens的正确性验证
- nvidia nim alias的正确性验证
- nvidia model passed的正确性验证
- 另有3个测试场景覆盖
- 影响模型提供者的可靠性和功能正确性

─────────────────────────────────────────────────────────────────
E2E tests: verify _build_kwargs_from_profile produces correct output.

These tests call _build_kwargs_from_profile on the transport directly,
without importing run_agent (which would cause xdist worker contamination)."""

import pytest
from agent.transports.chat_completions import ChatCompletionsTransport
from providers import get_provider_profile


@pytest.fixture
def transport():
    return ChatCompletionsTransport()


def _msgs():
    return [{"role": "user", "content": "hi"}]


class TestNvidiaProfileWiring:
    def test_nvidia_gets_default_max_tokens(self, transport):
        profile = get_provider_profile("nvidia")
        kwargs = transport.build_kwargs(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=_msgs(),
            tools=None,
            provider_profile=profile,
            max_tokens=None,
            max_tokens_param_fn=lambda x: {"max_tokens": x} if x else {},
            timeout=300,
            reasoning_config=None,
            request_overrides=None,
            session_id="test",
            ollama_num_ctx=None,
        )
        # NVIDIA profile sets default_max_tokens=16384
        assert kwargs.get("max_tokens") == 16384

    def test_nvidia_nim_alias(self, transport):
        profile = get_provider_profile("nvidia-nim")
        assert profile is not None
        assert profile.name == "nvidia"
        assert profile.default_max_tokens == 16384

    def test_nvidia_model_passed(self, transport):
        profile = get_provider_profile("nvidia")
        kwargs = transport.build_kwargs(
            model="nvidia/test-model",
            messages=_msgs(),
            tools=None,
            provider_profile=profile,
            max_tokens=None,
            max_tokens_param_fn=lambda x: {"max_tokens": x} if x else {},
            timeout=300,
            reasoning_config=None,
            request_overrides=None,
            session_id="test",
            ollama_num_ctx=None,
        )
        assert kwargs["model"] == "nvidia/test-model"

    def test_nvidia_messages_passed(self, transport):
        profile = get_provider_profile("nvidia")
        msgs = _msgs()
        kwargs = transport.build_kwargs(
            model="nvidia/test",
            messages=msgs,
            tools=None,
            provider_profile=profile,
            max_tokens=None,
            max_tokens_param_fn=lambda x: {"max_tokens": x} if x else {},
            timeout=300,
            reasoning_config=None,
            request_overrides=None,
            session_id="test",
            ollama_num_ctx=None,
        )
        assert kwargs["messages"] == msgs


class TestDeepSeekProfileWiring:
    def test_deepseek_no_forced_max_tokens(self, transport):
        profile = get_provider_profile("deepseek")
        kwargs = transport.build_kwargs(
            model="deepseek-chat",
            messages=_msgs(),
            tools=None,
            provider_profile=profile,
            max_tokens=None,
            max_tokens_param_fn=lambda x: {"max_tokens": x} if x else {},
            timeout=300,
            reasoning_config=None,
            request_overrides=None,
            session_id="test",
            ollama_num_ctx=None,
        )
        # DeepSeek has no default_max_tokens
        assert kwargs["model"] == "deepseek-chat"
        assert kwargs.get("max_tokens") is None or "max_tokens" not in kwargs

    def test_deepseek_messages_passed(self, transport):
        profile = get_provider_profile("deepseek")
        msgs = _msgs()
        kwargs = transport.build_kwargs(
            model="deepseek-chat",
            messages=msgs,
            tools=None,
            provider_profile=profile,
            max_tokens=None,
            max_tokens_param_fn=lambda x: {"max_tokens": x} if x else {},
            timeout=300,
            reasoning_config=None,
            request_overrides=None,
            session_id="test",
            ollama_num_ctx=None,
        )
        assert kwargs["messages"] == msgs
