"""工具输出预算配置

【产品经理理解要点】
控制每个工具返回给 LLM 的数据量上限，防止单次工具调用返回过多内容撑爆上下文窗口。
- 核心职责：定义三层预算——单次结果上限、单轮对话总预算、摘要预览长度；支持按工具名覆盖
- 关键业务概念：预算优先级——固定值 > 配置覆盖 > 注册表默认 > 全局默认，read_file 永不持久化（防无限循环）
- 在系统中的位置：tool_result_storage 的配置源，决定工具结果何时落盘、何时截断

─────────────────────────────────────────────────────────────────
Configurable budget constants for tool result persistence.

Per-tool resolution: pinned > config overrides > registry > default.
"""

from dataclasses import dataclass, field
from typing import Dict

# Tools whose thresholds must never be overridden.
# read_file=inf prevents infinite persist->read->persist loops.
PINNED_THRESHOLDS: Dict[str, float] = {
    "read_file": float("inf"),
}

# Defaults matching the current hardcoded values in tool_result_storage.py.
# Kept here as the single source of truth; tool_result_storage.py imports these.
DEFAULT_RESULT_SIZE_CHARS: int = 100_000
DEFAULT_TURN_BUDGET_CHARS: int = 200_000
DEFAULT_PREVIEW_SIZE_CHARS: int = 1_500


@dataclass(frozen=True)
class BudgetConfig:
    """Immutable budget constants for the 3-layer tool result persistence system.

    Layer 2 (per-result): resolve_threshold(tool_name) -> threshold in chars.
    Layer 3 (per-turn):   turn_budget -> aggregate char budget across all tool
                          results in a single assistant turn.
    Preview:              preview_size -> inline snippet size after persistence.
    """

    default_result_size: int = DEFAULT_RESULT_SIZE_CHARS
    turn_budget: int = DEFAULT_TURN_BUDGET_CHARS
    preview_size: int = DEFAULT_PREVIEW_SIZE_CHARS
    tool_overrides: Dict[str, int] = field(default_factory=dict)

    def resolve_threshold(self, tool_name: str) -> int | float:
        """Resolve the persistence threshold for a tool.

        Priority: pinned -> tool_overrides -> registry per-tool -> default.
        """
        if tool_name in PINNED_THRESHOLDS:
            return PINNED_THRESHOLDS[tool_name]
        if tool_name in self.tool_overrides:
            return self.tool_overrides[tool_name]
        from tools.registry import registry
        return registry.get_max_result_size(tool_name, default=self.default_result_size)


# Default config -- matches current hardcoded behavior exactly.
DEFAULT_BUDGET = BudgetConfig()
