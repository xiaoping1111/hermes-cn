"""命令行界面测试 - dashboard·browser·safe·导入

【产品经理理解要点】
验证命令行界面的导入功能
- 验证的功能: Static dashboard tests for browser-safe @nous-research/ui imports
- 核心测试场景: dashboard does not import nous ui root barrel
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Static dashboard tests for browser-safe @nous-research/ui imports.
"""
from pathlib import Path


WEB_SRC = Path(__file__).resolve().parents[2] / "web" / "src"


def test_dashboard_does_not_import_nous_ui_root_barrel():
    offenders = []
    for ext in ("*.tsx", "*.ts"):
        for path in WEB_SRC.rglob(ext):
            content = path.read_text(encoding="utf-8")
            if 'from "@nous-research/ui"' in content or "from '@nous-research/ui'" in content:
                offenders.append(str(path.relative_to(WEB_SRC)))

    assert offenders == []
