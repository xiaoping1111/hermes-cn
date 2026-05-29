"""命令行界面测试 - dashboard·多配置文件·nav·label

【产品经理理解要点】
验证命令行界面的多配置文件功能
- 验证的功能: Static dashboard tests for the Profiles navigation copy
- 核心测试场景: profiles nav label uses short copy
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
Static dashboard tests for the Profiles navigation copy.
"""
from pathlib import Path


def test_profiles_nav_label_uses_short_copy():
    en_i18n = Path(__file__).resolve().parents[2] / "web" / "src" / "i18n" / "en.ts"

    content = en_i18n.read_text(encoding="utf-8")

    # Nav label should be the clean short form, not the old verbose string
    assert 'profiles: "Profiles"' in content
    assert "profiles : multi agents" not in content
