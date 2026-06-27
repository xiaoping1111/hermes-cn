"""Agent运行引擎测试 - materialize data url cleanup

【产品经理理解要点】
智能体运行时的核心逻辑：流式响应、工具调用、上下文压缩、模型切换、中断处理等中的materialize data url cleanup验证。
- 验证功能：materialize data url cleanup功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：materialize data url cleanup功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression test: temp file cleanup when materializing data URLs for vision.

`_materialize_data_url_for_vision` creates a `NamedTemporaryFile(delete=False)`
so the path can be handed to vision backends.  If `base64.b64decode` raises on
a corrupt/unsupported data URL the temp file would otherwise persist forever
on disk, leaking once per failed call.
"""

from __future__ import annotations

import base64
import os
import tempfile
from pathlib import Path

import pytest

from run_agent import AIAgent


def _list_anthropic_tmpfiles(tmpdir: str) -> list[str]:
    return [
        name for name in os.listdir(tmpdir)
        if name.startswith("anthropic_image_")
    ]


def test_b64decode_failure_does_not_leak_tempfile(monkeypatch, tmp_path):
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))

    bad_url = "data:image/png;base64,!!!not-valid-base64!!!"
    with pytest.raises(Exception):
        AIAgent._materialize_data_url_for_vision(bad_url)

    leftovers = _list_anthropic_tmpfiles(str(tmp_path))
    assert leftovers == [], f"leaked temp files after decode failure: {leftovers}"


def test_successful_decode_returns_path_to_existing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))

    payload = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16  # a few bytes is enough
    encoded = base64.b64encode(payload).decode("ascii")
    good_url = f"data:image/png;base64,{encoded}"

    path_str, path_obj = AIAgent._materialize_data_url_for_vision(good_url)

    assert isinstance(path_obj, Path)
    assert path_obj.exists()
    assert path_obj.read_bytes() == payload
    assert path_str == str(path_obj)
    # Caller is responsible for cleanup; mimic that here so the test leaves
    # no artifacts behind.
    path_obj.unlink()
