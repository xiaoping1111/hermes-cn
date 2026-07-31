"""Agent核心测试 - minimax auxiliary url

【产品经理理解要点】
Agent核心模块：Prompt构建、上下文压缩、模型路由、凭证池、记忆、LSP等中的minimax auxiliary url验证。
- 验证功能：minimax auxiliary url功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：minimax auxiliary url功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for MiniMax auxiliary client URL normalization.

MiniMax and MiniMax-CN set inference_base_url to the /anthropic path.
The auxiliary client uses the OpenAI SDK, which needs /v1 instead.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from agent.auxiliary_client import _to_openai_base_url


class TestToOpenaiBaseUrl:
    def test_minimax_global_anthropic_suffix_replaced(self):
        assert _to_openai_base_url("https://api.minimax.io/anthropic") == "https://api.minimax.io/v1"








    def test_none(self):
        assert _to_openai_base_url(None) == ""
