"""打包元数据测试

【产品经理理解要点】
验证pyproject.toml中的打包配置，确保依赖声明和文件包含列表正确。
- faster-whisper不在基础依赖中（仅语音可选依赖）
- MANIFEST.in包含技能文件
- 影响pip安装的包完整性
"""

from pathlib import Path
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_faster_whisper_is_not_a_base_dependency():
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    deps = data["project"]["dependencies"]

    assert not any(dep.startswith("faster-whisper") for dep in deps)

    voice_extra = data["project"]["optional-dependencies"]["voice"]
    assert any(dep.startswith("faster-whisper") for dep in voice_extra)


def test_manifest_includes_bundled_skills():
    manifest = (REPO_ROOT / "MANIFEST.in").read_text(encoding="utf-8")

    assert "graft skills" in manifest
    assert "graft optional-skills" in manifest
