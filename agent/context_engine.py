"""上下文引擎抽象基类 — 定义对话压缩的标准接口

【产品经理理解要点】
这个模块定义了"上下文引擎"的标准接口。上下文引擎是控制对话长度的策略层：
当对话超过 AI 的记忆容量时，由上下文引擎决定如何压缩。

默认实现是 ContextCompressor（用辅助模型做摘要），但通过这个抽象接口，
可以替换为其他策略（如基于图的长期记忆系统），而不需要改 Agent 核心代码。

生命周期：
  创建引擎 → 注册到Agent → 会话开始(on_session_start)
  → 每次AI响应后更新token统计(update_from_response)
  → 每轮结束时检查是否需要压缩(should_compress)
  → 需要时执行压缩(compress)

就像手机内存管理策略：可以选"杀后台"策略，也可以选"压缩缓存"策略，
接口统一，策略可换。

─────────────────────────────────────────────────────────────────

可插拔上下文引擎的抽象基类。

上下文引擎控制当对话接近模型的 token 限制时如何管理上下文。
内置的 `ContextCompressor` 是默认实现。

引擎的主要职责包括：
  - 决定何时触发压缩（Compaction）
  - 执行压缩操作（如总结、丢弃旧消息、构建 DAG 等）
  - 可选地向代理公开工具（如 lcm_grep）
  - 跟踪 API 响应中的 token 使用情况

生命周期：
  1. 实例化并注册。
  2. `on_session_start()`: 会话开始时调用。
  3. `update_from_response()`: 每次 API 响应后调用，更新 token 统计。
  4. `should_compress()`: 每一轮结束后检查是否需要压缩。
  5. `compress()`: 当需要压缩时调用，返回缩减后的消息列表。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ContextEngine(ABC):
    """Base class all context engines must implement."""

    # -- Identity ----------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier (e.g. 'compressor', 'lcm')."""

    # -- Token state (read by run_agent.py for display/logging) ------------
    #
    # Engines MUST maintain these. run_agent.py reads them directly.

    last_prompt_tokens: int = 0
    last_completion_tokens: int = 0
    last_total_tokens: int = 0
    threshold_tokens: int = 0
    context_length: int = 0
    compression_count: int = 0

    # -- Compaction parameters (read by run_agent.py for preflight) --------
    #
    # These control the preflight compression check.  Subclasses may
    # override via __init__ or property; defaults are sensible for most
    # engines.
    #
    # protect_first_n semantics (since PR #13754): count of non-system head
    # messages always preserved verbatim, IN ADDITION to the system prompt
    # which is always implicitly protected.  Default 3 keeps the
    # historical "system + first 3 non-system messages" head shape.

    threshold_percent: float = 0.75
    protect_first_n: int = 3
    protect_last_n: int = 6

    # -- Core interface ----------------------------------------------------

    @abstractmethod
    def update_from_response(self, usage: Dict[str, Any]) -> None:
        """Update tracked token usage from an API response.

        Called after every LLM call with the usage dict from the response.
        """

    @abstractmethod
    def should_compress(self, prompt_tokens: int = None) -> bool:
        """Return True if compaction should fire this turn."""

    @abstractmethod
    def compress(
        self,
        messages: List[Dict[str, Any]],
        current_tokens: int = None,
        focus_topic: str = None,
    ) -> List[Dict[str, Any]]:
        """Compact the message list and return the new message list.

        This is the main entry point. The engine receives the full message
        list and returns a (possibly shorter) list that fits within the
        context budget. The implementation is free to summarize, build a
        DAG, or do anything else — as long as the returned list is a valid
        OpenAI-format message sequence.

        Args:
            focus_topic: Optional topic string from manual ``/compress <focus>``.
                Engines that support guided compression should prioritise
                preserving information related to this topic.  Engines that
                don't support it may simply ignore this argument.
        """

    # -- Optional: pre-flight check ----------------------------------------

    def should_compress_preflight(self, messages: List[Dict[str, Any]]) -> bool:
        """Quick rough check before the API call (no real token count yet).

        Default returns False (skip pre-flight). Override if your engine
        can do a cheap estimate.
        """
        return False

    # -- Optional: manual /compress preflight ------------------------------

    def has_content_to_compress(self, messages: List[Dict[str, Any]]) -> bool:
        """Quick check: is there anything in ``messages`` that can be compacted?

        Used by the gateway ``/compress`` command as a preflight guard —
        returning False lets the gateway report "nothing to compress yet"
        without making an LLM call.

        Default returns True (always attempt).  Engines with a cheap way
        to introspect their own head/tail boundaries should override this
        to return False when the transcript is still entirely protected.
        """
        return True

    # -- Optional: session lifecycle ---------------------------------------

    def on_session_start(self, session_id: str, **kwargs) -> None:
        """Called when a new conversation session begins.

        Use this to load persisted state (DAG, store) for the session.
        kwargs may include hermes_home, platform, model, etc.
        """

    def on_session_end(self, session_id: str, messages: List[Dict[str, Any]]) -> None:
        """Called at real session boundaries (CLI exit, /reset, gateway expiry).

        Use this to flush state, close DB connections, etc.
        NOT called per-turn — only when the session truly ends.
        """

    def on_session_reset(self) -> None:
        """Called on /new or /reset. Reset per-session state.

        Default resets compression_count and token tracking.
        """
        self.last_prompt_tokens = 0
        self.last_completion_tokens = 0
        self.last_total_tokens = 0
        self.compression_count = 0

    # -- Optional: tools ---------------------------------------------------

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas this engine provides to the agent.

        Default returns empty list (no tools). LCM would return schemas
        for lcm_grep, lcm_describe, lcm_expand here.
        """
        return []

    def handle_tool_call(self, name: str, args: Dict[str, Any], **kwargs) -> str:
        """Handle a tool call from the agent.

        Only called for tool names returned by get_tool_schemas().
        Must return a JSON string.

        kwargs may include:
          messages: the current in-memory message list (for live ingestion)
        """
        import json
        return json.dumps({"error": f"Unknown context engine tool: {name}"})

    # -- Optional: status / display ----------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Return status dict for display/logging.

        Default returns the standard fields run_agent.py expects.
        """
        return {
            "last_prompt_tokens": self.last_prompt_tokens,
            "threshold_tokens": self.threshold_tokens,
            "context_length": self.context_length,
            "usage_percent": (
                min(100, self.last_prompt_tokens / self.context_length * 100)
                if self.context_length else 0
            ),
            "compression_count": self.compression_count,
        }

    # -- Optional: model switch support ------------------------------------

    def update_model(
        self,
        model: str,
        context_length: int,
        base_url: str = "",
        api_key: str = "",
        provider: str = "",
    ) -> None:
        """Called when the user switches models or on fallback activation.

        Default updates context_length and recalculates threshold_tokens
        from threshold_percent. Override if your engine needs more
        (e.g. recalculate DAG budgets, switch summary models).
        """
        self.context_length = context_length
        self.threshold_tokens = int(context_length * self.threshold_percent)
