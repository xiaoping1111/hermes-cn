"""工具系统测试 - tts path traversal

【产品经理理解要点】
工具层（MCP/浏览器/文件/图片/搜索/终端/TTS/审批等）的安全性与功能正确性中的tts path traversal验证。
- 验证功能：tts path traversal功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：tts path traversal功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression: text_to_speech_tool output_path must reject '..' traversal.

The TTS surface accepts agent/user-supplied absolute paths (writing to a
chosen file is the whole point). What it must reject is paths that use
``..`` components to escape their declared base — those are almost
always either a bug or prompt-injection-controlled
(e.g. ``output_path="audio/../../etc/cron.d/x"``).
"""

import json

from tools.tts_tool import text_to_speech_tool


def test_output_path_rejects_traversal_escape():
    """A path with '..' components must be rejected before any provider work."""
    result = json.loads(text_to_speech_tool(
        text="hello",
        output_path="audio/../../etc/cron.d/malicious",
    ))
    assert result["success"] is False
    assert "traversal" in result["error"].lower()


def test_output_path_rejects_bare_dotdot():
    """Bare '..' prefix must be rejected."""
    result = json.loads(text_to_speech_tool(
        text="hello",
        output_path="../escape.mp3",
    ))
    assert result["success"] is False
    assert "traversal" in result["error"].lower()


def test_output_path_rejects_hermes_oauth_store(tmp_path, monkeypatch):
    """TTS output_path must not bypass the shared protected-file write guard."""
    import agent.file_safety as file_safety

    hermes_home = tmp_path / "hermes-home"
    hermes_home.mkdir()
    monkeypatch.setattr(file_safety, "_hermes_home_path", lambda: hermes_home)
    monkeypatch.setattr(file_safety, "_hermes_root_path", lambda: hermes_home)

    target = hermes_home / ".anthropic_oauth.json"
    result = json.loads(text_to_speech_tool(
        text="hello",
        output_path=str(target),
    ))

    assert result["success"] is False
    assert "protected credential" in result["error"]
    assert not target.exists()


def test_output_path_rejects_mcp_token_directory(tmp_path, monkeypatch):
    """TTS output_path must not write synthesized audio over MCP token files."""
    import agent.file_safety as file_safety

    hermes_home = tmp_path / "hermes-home"
    token_dir = hermes_home / "mcp-tokens"
    token_dir.mkdir(parents=True)
    monkeypatch.setattr(file_safety, "_hermes_home_path", lambda: hermes_home)
    monkeypatch.setattr(file_safety, "_hermes_root_path", lambda: hermes_home)

    target = token_dir / "server.mp3"
    result = json.loads(text_to_speech_tool(
        text="hello",
        output_path=str(target),
    ))

    assert result["success"] is False
    assert "protected credential" in result["error"]
    assert not target.exists()
