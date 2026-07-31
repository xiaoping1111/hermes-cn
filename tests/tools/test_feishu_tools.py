"""飞书工具系统测试

【产品经理理解要点】
飞书平台工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性。
- 验证功能：飞书平台功能验证
- 关键场景：飞书消息收发、连接管理
- 业务影响：飞书平台功能不可用

─────────────────────────────────────────────────────────────────────────
Tests for feishu_doc_tool and feishu_drive_tool — registration and schema validation.
"""

import importlib
import unittest

from tools.registry import registry

# Trigger tool discovery so feishu tools get registered
importlib.import_module("tools.feishu_doc_tool")
importlib.import_module("tools.feishu_drive_tool")


class TestFeishuToolRegistration(unittest.TestCase):
    """Verify feishu tools are registered and have valid schemas."""

    EXPECTED_TOOLS = {
        "feishu_doc_read": "feishu_doc",
        "feishu_drive_list_comments": "feishu_drive",
        "feishu_drive_list_comment_replies": "feishu_drive",
        "feishu_drive_reply_comment": "feishu_drive",
        "feishu_drive_add_comment": "feishu_drive",
    }

    def test_all_tools_registered(self):
        for tool_name, toolset in self.EXPECTED_TOOLS.items():
            entry = registry.get_entry(tool_name)
            self.assertIsNotNone(entry, f"{tool_name} not registered")
            self.assertEqual(entry.toolset, toolset)


    def test_drive_tools_require_file_token(self):
        for tool_name in self.EXPECTED_TOOLS:
            if tool_name == "feishu_doc_read":
                continue
            entry = registry.get_entry(tool_name)
            props = entry.schema["parameters"].get("properties", {})
            self.assertIn("file_token", props, f"{tool_name} missing file_token param")
            self.assertIn("file_type", props, f"{tool_name} missing file_type param")


if __name__ == "__main__":
    unittest.main()
