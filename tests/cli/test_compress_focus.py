"""聚焦压缩测试

【产品经理理解要点】
验证带主题焦点的上下文压缩功能，确保压缩保留与指定主题相关的内容。
- 焦点主题对压缩摘要内容的影响
- 非焦点内容的合理裁剪
- 影响长对话中保留重要上下文的能力

──────────────────────────────────────────────────────────────
Tests for /compress <focus> — guided compression with focus topic.

Inspired by Claude Code's /compact <focus> feature.
"""

from unittest.mock import MagicMock, patch

from tests.cli.test_cli_init import _make_cli


def _make_history() -> list[dict[str, str]]:
    return [
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
        {"role": "assistant", "content": "four"},
    ]


def test_focus_topic_extracted_and_passed(capsys):
    """Focus topic is extracted from the command and passed to _compress_context."""
    shell = _make_cli()
    history = _make_history()
    compressed = [history[0], history[-1]]
    shell.conversation_history = history
    shell.agent = MagicMock()
    shell.agent.compression_enabled = True
    shell.agent._cached_system_prompt = ""
    shell.agent._compress_context.return_value = (compressed, "")

    def _estimate(messages):
        if messages is history:
            return 100
        return 50

    with patch("agent.model_metadata.estimate_messages_tokens_rough", side_effect=_estimate):
        shell._manual_compress("/compress database schema")

    output = capsys.readouterr().out
    assert 'focus: "database schema"' in output

    # Verify focus_topic was passed through
    shell.agent._compress_context.assert_called_once()
    call_kwargs = shell.agent._compress_context.call_args
    assert call_kwargs.kwargs.get("focus_topic") == "database schema"


def test_no_focus_topic_when_bare_command(capsys):
    """When no focus topic is provided, None is passed."""
    shell = _make_cli()
    history = _make_history()
    shell.conversation_history = history
    shell.agent = MagicMock()
    shell.agent.compression_enabled = True
    shell.agent._cached_system_prompt = ""
    shell.agent._compress_context.return_value = (list(history), "")

    with patch("agent.model_metadata.estimate_messages_tokens_rough", return_value=100):
        shell._manual_compress("/compress")

    shell.agent._compress_context.assert_called_once()
    call_kwargs = shell.agent._compress_context.call_args
    assert call_kwargs.kwargs.get("focus_topic") is None


def test_empty_focus_after_command_treated_as_none(capsys):
    """Trailing whitespace after /compress does not produce a focus topic."""
    shell = _make_cli()
    history = _make_history()
    shell.conversation_history = history
    shell.agent = MagicMock()
    shell.agent.compression_enabled = True
    shell.agent._cached_system_prompt = ""
    shell.agent._compress_context.return_value = (list(history), "")

    with patch("agent.model_metadata.estimate_messages_tokens_rough", return_value=100):
        shell._manual_compress("/compress   ")

    shell.agent._compress_context.assert_called_once()
    call_kwargs = shell.agent._compress_context.call_args
    assert call_kwargs.kwargs.get("focus_topic") is None


def test_focus_topic_printed_in_compression_banner(capsys):
    """The focus topic shows in the compression progress banner."""
    shell = _make_cli()
    history = _make_history()
    compressed = [history[0], history[-1]]
    shell.conversation_history = history
    shell.agent = MagicMock()
    shell.agent.compression_enabled = True
    shell.agent._cached_system_prompt = ""
    shell.agent._compress_context.return_value = (compressed, "")

    with patch("agent.model_metadata.estimate_messages_tokens_rough", return_value=100):
        shell._manual_compress("/compress API endpoints")

    output = capsys.readouterr().out
    assert 'focus: "API endpoints"' in output


def test_no_focus_prints_standard_banner(capsys):
    """Without focus, the standard banner (no focus: line) is printed."""
    shell = _make_cli()
    history = _make_history()
    compressed = [history[0], history[-1]]
    shell.conversation_history = history
    shell.agent = MagicMock()
    shell.agent.compression_enabled = True
    shell.agent._cached_system_prompt = ""
    shell.agent._compress_context.return_value = (compressed, "")

    with patch("agent.model_metadata.estimate_messages_tokens_rough", return_value=100):
        shell._manual_compress("/compress")

    output = capsys.readouterr().out
    assert "focus:" not in output
    assert "Compressing" in output
