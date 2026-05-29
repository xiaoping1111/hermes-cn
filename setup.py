"""Hermes Agent安装配置

【产品经理理解要点】
Python包安装配置，确保skills和optional-skills目录被正确打包到安装包中。
- 核心职责：声明需要随pip install一起安装的数据文件（技能目录）
- 技能打包：递归扫描skills/和optional-skills/目录，确保用户安装后技能可用
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from setuptools import setup


REPO_ROOT = Path(__file__).parent.resolve()


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
    data_files=[
        *_data_file_tree("skills"),
        *_data_file_tree("optional-skills"),
    ]
)
