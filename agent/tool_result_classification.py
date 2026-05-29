"""工具结果分类 — 判断工具执行是否成功修改了文件

【产品经理理解要点】
这个模块做一件简单但重要的事：判断"写文件"或"打补丁"操作是否真正生效了。

为什么需要判断？因为 AI 调用写文件工具后，有时会返回错误（权限不足、路径不对）。
这个模块通过检查返回结果中的关键字段，准确判断文件是否被成功修改，
从而让护栏系统（tool_guardrails）能正确统计文件变更次数。

─────────────────────────────────────────────────────────────────

Shared helpers for classifying tool result payloads.
"""

from __future__ import annotations

import json
from typing import Any


FILE_MUTATING_TOOL_NAMES = frozenset({"write_file", "patch"})


def file_mutation_result_landed(tool_name: str, result: Any) -> bool:
    """Return True when a file mutation result proves the write landed."""
    if tool_name not in FILE_MUTATING_TOOL_NAMES or not isinstance(result, str):
        return False
    try:
        data = json.loads(result.strip())
    except Exception:
        return False
    if not isinstance(data, dict) or data.get("error"):
        return False
    if tool_name == "write_file":
        return "bytes_written" in data
    if tool_name == "patch":
        return data.get("success") is True
    return False
