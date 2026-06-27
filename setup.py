from __future__ import annotations

"""项目打包构建配置

【产品经理理解要点】
setuptools 构建脚本：定义 pip install 时的包结构和构建步骤，支持只读源码树构建。
- 核心职责：收集子包、生成 entry_points、处理只读源码树时的临时构建目录
- 关键业务概念：pip 可安装包、命令行入口点(hermes/hermes-agent)、只读构建模式
- 在系统中的位置：项目发布基础设施，执行 pip install -e . 时运行

─────────────────────────────────────────────────────────────────
"""

from collections import defaultdict
from pathlib import Path
import tempfile

from setuptools import setup
from setuptools.command.build import build as _build
from setuptools.command.egg_info import egg_info as _egg_info


REPO_ROOT = Path(__file__).parent.resolve()


def _source_tree_is_writable() -> bool:
    probe = REPO_ROOT / ".setuptools-write-probe"
    try:
        with probe.open("w", encoding="utf-8") as handle:
            handle.write("")
        probe.unlink()
    except OSError:
        try:
            probe.unlink(missing_ok=True)
        except OSError:
            pass
        return False
    return True


def _temporary_build_dir(kind: str) -> str:
    return tempfile.mkdtemp(prefix=f"hermes-agent-{kind}-")


def _would_write_under_source(path_value: str | None) -> bool:
    if path_value is None:
        return True
    path = Path(path_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    try:
        path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return False
    return True


class ReadOnlySourceBuild(_build):
    def finalize_options(self) -> None:
        if (
            not _source_tree_is_writable()
            and _would_write_under_source(self.build_base)
        ):
            self.build_base = _temporary_build_dir("build")
        super().finalize_options()


class ReadOnlySourceEggInfo(_egg_info):
    def finalize_options(self) -> None:
        if (
            not _source_tree_is_writable()
            and _would_write_under_source(self.egg_base)
        ):
            self.egg_base = _temporary_build_dir("egg-info")
        super().finalize_options()


def _data_file_tree(root_name: str) -> list[tuple[str, list[str]]]:
    root = REPO_ROOT / root_name
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(REPO_ROOT)
        grouped[str(rel_path.parent)].append(str(rel_path))
    return sorted(grouped.items())


setup(
    cmdclass={
        "build": ReadOnlySourceBuild,
        "egg_info": ReadOnlySourceEggInfo,
    },
    data_files=[
        *_data_file_tree("skills"),
        *_data_file_tree("optional-skills"),
    ]
)
