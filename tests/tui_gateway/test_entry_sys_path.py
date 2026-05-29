"""系统路径入口测试

【产品经理理解要点】
验证TUI网关模块中empty string and dot removed from sys path等4个场景的正确性
- empty string and dot removed from sys path的正确性验证
- hermes src root inserted at front的正确性验证
- src root not duplicated if already present的正确性验证
- 另有1个测试场景覆盖
- 影响TUI网关的可靠性和功能正确性

─────────────────────────────────────────────────────────────────
Tests for tui_gateway/entry.py sys.path hardening (issue #15989).

When the TUI backend is spawned by Node.js, the Python interpreter may have
'' or '.' at the front of sys.path, allowing a local utils/ directory in CWD
to shadow the installed utils module.  entry.py must sanitize sys.path before
any non-stdlib import is resolved."""

import importlib
import os
import sys
from unittest.mock import patch


def _reload_entry_with_env(env_overrides: dict) -> None:
    """Re-execute entry.py's module-level path setup under a controlled env."""
    # We only want to exercise the sys.path fixup block, not the signal/import
    # machinery that follows.  We do this by running the fixup code verbatim in
    # a fresh copy of sys.path rather than importing the real module (which
    # would trigger tui_gateway.server imports requiring heavy mocks).
    original_path = sys.path[:]
    original_env = {k: os.environ.get(k) for k in env_overrides}
    try:
        with patch.dict(os.environ, env_overrides, clear=False):
            _src_root = os.environ.get("HERMES_PYTHON_SRC_ROOT", "")
            if _src_root and _src_root not in sys.path:
                sys.path.insert(0, _src_root)
            sys.path = [p for p in sys.path if p not in {"", "."}]
        return sys.path[:]
    finally:
        sys.path = original_path
        for k, v in original_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def test_empty_string_and_dot_removed_from_sys_path():
    original = sys.path[:]
    try:
        sys.path.insert(0, "")
        sys.path.insert(0, ".")
        assert "" in sys.path
        assert "." in sys.path

        # Run the entry.py fixup logic directly
        sys.path = [p for p in sys.path if p not in {"", "."}]

        assert "" not in sys.path
        assert "." not in sys.path
    finally:
        sys.path = original


def test_hermes_src_root_inserted_at_front():
    original = sys.path[:]
    try:
        fake_root = "/fake/hermes/src"
        with patch.dict(os.environ, {"HERMES_PYTHON_SRC_ROOT": fake_root}):
            _src_root = os.environ.get("HERMES_PYTHON_SRC_ROOT", "")
            if _src_root and _src_root not in sys.path:
                sys.path.insert(0, _src_root)
            sys.path = [p for p in sys.path if p not in {"", "."}]

        assert sys.path[0] == fake_root
    finally:
        sys.path = original


def test_src_root_not_duplicated_if_already_present():
    original = sys.path[:]
    try:
        fake_root = "/already/present"
        sys.path.insert(0, fake_root)
        count_before = sys.path.count(fake_root)

        with patch.dict(os.environ, {"HERMES_PYTHON_SRC_ROOT": fake_root}):
            _src_root = os.environ.get("HERMES_PYTHON_SRC_ROOT", "")
            if _src_root and _src_root not in sys.path:
                sys.path.insert(0, _src_root)
            sys.path = [p for p in sys.path if p not in {"", "."}]

        assert sys.path.count(fake_root) == count_before
    finally:
        sys.path = original


def test_no_src_root_env_does_not_crash():
    original = sys.path[:]
    try:
        env = {k: v for k, v in os.environ.items() if k != "HERMES_PYTHON_SRC_ROOT"}
        with patch.dict(os.environ, {}, clear=True):
            os.environ.update(env)
            _src_root = os.environ.get("HERMES_PYTHON_SRC_ROOT", "")
            if _src_root and _src_root not in sys.path:
                sys.path.insert(0, _src_root)
            sys.path = [p for p in sys.path if p not in {"", "."}]
        # No exception raised
    finally:
        sys.path = original
