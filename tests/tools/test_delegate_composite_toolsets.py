"""工具系统测试 - delegate composite toolsets

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的delegate composite toolsets验证。
- 验证功能：delegate composite toolsets功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：delegate composite toolsets功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Tests for composite toolset expansion in delegate_task intersection.
"""

import unittest

from tools.delegate_tool import _expand_parent_toolsets


class TestExpandParentToolsets(unittest.TestCase):
    """Verify _expand_parent_toolsets recognises individual toolsets within composites."""

    def test_composite_hermes_cli_expands_web(self):
        """hermes-cli includes web_search/web_extract → 'web' should be in expansion."""
        expanded = _expand_parent_toolsets({"hermes-cli"})
        self.assertIn("web", expanded)
        self.assertIn("terminal", expanded)
        self.assertIn("browser", expanded)
        # Original composite is preserved
        self.assertIn("hermes-cli", expanded)


    def test_intersection_with_expanded_composite(self):
        """End-to-end: requesting ['web'] from parent with ['hermes-cli'] yields ['web']."""
        parent_toolsets = {"hermes-cli"}
        expanded = _expand_parent_toolsets(parent_toolsets)
        toolsets = ["web"]
        child_toolsets = [t for t in toolsets if t in expanded]
        self.assertEqual(child_toolsets, ["web"])


if __name__ == "__main__":
    unittest.main()
