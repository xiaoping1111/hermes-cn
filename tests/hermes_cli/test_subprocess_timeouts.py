"""命令行界面测试 - subprocess·超时控制

【产品经理理解要点】
验证命令行界面的超时控制功能
- 验证的功能: Tests for subprocess.run() timeout coverage in CLI utilities
- 核心测试场景: all subprocess run calls have timeout
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Tests for subprocess.run() timeout coverage in CLI utilities.
"""
import ast
from pathlib import Path

import pytest


# Parameterise over every CLI module that calls subprocess.run
_CLI_MODULES = [
    "hermes_cli/doctor.py",
    "hermes_cli/status.py",
    "hermes_cli/clipboard.py",
    "hermes_cli/banner.py",
]


def _subprocess_run_calls(filepath: str) -> list[dict]:
    """Parse a Python file and return info about subprocess.run() calls."""
    source = Path(filepath).read_text()
    tree = ast.parse(source, filename=filepath)
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (isinstance(func, ast.Attribute) and func.attr == "run"
                and isinstance(func.value, ast.Name)
                and func.value.id == "subprocess"):
            has_timeout = any(kw.arg == "timeout" for kw in node.keywords)
            calls.append({"line": node.lineno, "has_timeout": has_timeout})
    return calls


@pytest.mark.parametrize("filepath", _CLI_MODULES)
def test_all_subprocess_run_calls_have_timeout(filepath):
    """Every subprocess.run() call in CLI modules must specify a timeout."""
    if not Path(filepath).exists():
        pytest.skip(f"{filepath} not found")
    calls = _subprocess_run_calls(filepath)
    missing = [c for c in calls if not c["has_timeout"]]
    assert not missing, (
        f"{filepath} has subprocess.run() without timeout at "
        f"line(s): {[c['line'] for c in missing]}"
    )
