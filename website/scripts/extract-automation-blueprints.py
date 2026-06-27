#!/usr/bin/env python3
"""自动化蓝图目录生成

【产品经理理解要点】
从代码中提取自动化蓝图（定时任务模板）的元数据，生成 JSON 目录供文档站点展示。
- 核心职责：导入蓝图定义，输出 JSON 数组供文档页渲染为卡片（含描述、调度、斜杠命令、深链接）
- 关键概念：蓝图的单一数据源在 cron/blueprint_catalog.py，本脚本仅做格式转换
- 系统定位：文档构建脚本，由 prebuild.mjs 在 npm start/build 前自动调用

─────────────────────────────────────────────────────────────────
Generate the Automation Blueprints catalog JSON for the docs site.

Mirrors ``extract-skills.py``: imports the single-source-of-truth blueprint
definitions from ``cron/blueprint_catalog.py`` and emits a flat JSON array the
docs page renders into cards (description, schedule, copy-paste slash command,
and a ``hermes://`` "Send to App" deep-link).

Output: ``website/static/api/automation-blueprints-index.json`` (served at
``/docs/api/automation-blueprints-index.json``). Run automatically by
``website/scripts/prebuild.mjs`` before ``npm start`` / ``npm run build``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Repo root = two levels up from website/scripts/.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

OUTPUT = REPO_ROOT / "website" / "static" / "api" / "automation-blueprints-index.json"


def build_index() -> list:
    from cron.blueprint_catalog import CATALOG, blueprint_catalog_entry

    return [blueprint_catalog_entry(r) for r in CATALOG]


def main() -> int:
    try:
        index = build_index()
    except Exception as e:  # pragma: no cover - import/build failure
        # Match extract-skills.py's resilience: write an empty array so the
        # docs build never hard-fails on a generator hiccup.
        sys.stderr.write(f"extract-automation-blueprints: {e}; writing empty index\n")
        index = []

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(index, f, separators=(",", ":"))
    sys.stderr.write(f"extract-automation-blueprints: wrote {len(index)} blueprints -> {OUTPUT}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
