"""Agent运行引擎测试 - strip reasoning tags cli

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的strip reasoning tags cli验证。
- 验证功能：strip reasoning tags cli功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：strip reasoning tags cli功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for cli.py::_strip_reasoning_tags — specifically the tool-call
XML stripping added in openclaw/openclaw#67318 port.

The CLI has its own copy of the stripper because it needs to run on the
final displayed assistant text (after streaming) without depending on the
AIAgent instance. It must stay in sync with run_agent.py::_strip_think_blocks
for tool-call tag coverage.
"""


from cli import _strip_reasoning_tags


class TestToolCallStripping:
    def test_tool_call_block_stripped(self):
        text = '<tool_call>{"name": "x"}</tool_call>result'
        result = _strip_reasoning_tags(text)
        assert "<tool_call>" not in result
        assert "result" in result







    def test_empty_string(self):
        assert _strip_reasoning_tags("") == ""

