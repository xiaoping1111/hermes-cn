"""命令行界面测试 - 技能系统·subparser

【产品经理理解要点】
验证命令行界面的技能系统功能
- 验证的功能: Test that skills subparser doesn't conflict (regression test for #898)
- 核心测试场景: no duplicate skills subparser
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Test that skills subparser doesn't conflict (regression test for #898).
"""

import argparse


def test_no_duplicate_skills_subparser():
    """Ensure 'skills' subparser is only registered once to avoid Python 3.11+ crash.

    Python 3.11 changed argparse to raise an exception on duplicate subparser
    names instead of silently overwriting (see CPython #94331).

    This test will fail with:
        argparse.ArgumentError: argument command: conflicting subparser: skills

    if the duplicate 'skills' registration is reintroduced.
    """
    # Force fresh import of the module where parser is constructed
    # If there are duplicate 'skills' subparsers, this import will raise
    # argparse.ArgumentError at module load time
    import importlib
    import sys

    # Remove cached module if present
    if 'hermes_cli.main' in sys.modules:
        del sys.modules['hermes_cli.main']

    try:
        import hermes_cli.main  # noqa: F401
    except argparse.ArgumentError as e:
        if "conflicting subparser" in str(e):
            raise AssertionError(
                f"Duplicate subparser detected: {e}. "
                "See issue #898 for details."
            ) from e
        raise
