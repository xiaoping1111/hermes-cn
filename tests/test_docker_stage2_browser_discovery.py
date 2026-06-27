"""测试 - docker stage2 browser discovery

【产品经理理解要点】
功能验证中的docker stage2 browser discovery验证。
- 验证功能：docker stage2 browser discovery功能正确性验证
- 关键场景：核心逻辑、边界条件、错误处理
- 业务影响：docker stage2 browser discovery功能异常或存在安全隐患

─────────────────────────────────────────────────────────────────────────
Regression tests for Docker stage2 browser executable discovery.
"""

from pathlib import Path


def test_stage2_discovers_playwright_arm64_headless_shell() -> None:
    """Playwright's --only-shell layout may use a headless_shell basename."""
    script = Path("docker/stage2-hook.sh").read_text()

    assert "-name 'headless_shell'" in script


def test_stage2_discovery_stays_filename_matched() -> None:
    """Avoid broad path grep that can pick executable shared libraries."""
    script = Path("docker/stage2-hook.sh").read_text()

    discovery_block = script.split("browser_bin=$(", 1)[1].split(")\n    if", 1)[0]
    assert "find \"$PLAYWRIGHT_BROWSERS_PATH\" -type f -executable" in discovery_block
    assert "grep" not in discovery_block
