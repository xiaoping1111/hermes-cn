"""CLIdashboard browser safe imports测试

【产品经理理解要点】
CLIdashboard browser safe imports功能测试。
- 验证功能：命令行dashboard browser safe imports功能
- 关键场景：配置、执行、验证
- 业务影响：dashboard browser safe imports命令行功能失效

─────────────────────────────────────────────────────────────────────────
Static dashboard tests for browser-safe @nous-research/ui imports."""
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
