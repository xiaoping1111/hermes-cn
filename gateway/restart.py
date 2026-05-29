"""网关重启常量 — 优雅重启时的等待超时和退出码

【产品经理理解要点】
网关重启时不会立即停止，而是等待当前对话完成后再重启。
这个模块定义了等待超时时间和重启退出码。

─────────────────────────────────────────────────────────────────

Shared gateway restart constants and parsing helpers."""

from hermes_cli.config import DEFAULT_CONFIG

# EX_TEMPFAIL from sysexits.h — used to ask the service manager to restart
# the gateway after a graceful drain/reload path completes.
GATEWAY_SERVICE_RESTART_EXIT_CODE = 75

DEFAULT_GATEWAY_RESTART_DRAIN_TIMEOUT = float(
    DEFAULT_CONFIG["agent"]["restart_drain_timeout"]
)


def parse_restart_drain_timeout(raw: object) -> float:
    """Parse a configured drain timeout, falling back to the shared default."""
    try:
        value = float(raw) if str(raw or "").strip() else DEFAULT_GATEWAY_RESTART_DRAIN_TIMEOUT
    except (TypeError, ValueError):
        return DEFAULT_GATEWAY_RESTART_DRAIN_TIMEOUT
    return max(0.0, value)
