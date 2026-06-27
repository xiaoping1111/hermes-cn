"""CLIdashboard profiles nav label测试

【产品经理理解要点】
CLIdashboard profiles nav label功能测试。
- 验证功能：命令行dashboard profiles nav label功能
- 关键场景：配置、执行、验证
- 业务影响：dashboard profiles nav label命令行功能失效

─────────────────────────────────────────────────────────────────────────
Static dashboard tests for the Profiles navigation copy."""
from pathlib import Path


def test_profiles_nav_label_uses_short_copy():
    en_i18n = Path(__file__).resolve().parents[2] / "web" / "src" / "i18n" / "en.ts"

    content = en_i18n.read_text(encoding="utf-8")

    # Nav label should be the clean short form, not the old verbose string
    assert 'profiles: "Profiles"' in content
    assert "profiles : multi agents" not in content
