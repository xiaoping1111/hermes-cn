
"""子命令构建器包

【产品经理理解要点】
CLI子命令解析器构建器包，从main.py的god-file中拆分而来。
- 每个子命令组在独立模块中拥有build_*_parser函数
- 处理器(cmd_*)仍留在main.py通过依赖注入避免循环导入
- Phase 2 god-file分解方案的产物

────────────────────────────────────────────────────────────────"""

"""CLI subcommand parser builders for ``hermes <subcommand>``.

``hermes_cli/main.py:main()`` historically built the entire argparse tree
inline — 179 ``add_parser`` calls across ~26 subcommand groups, all wedged
into one 3,300-line function. This package breaks that tree apart: each
subcommand group owns a ``build_<group>_parser(subparsers, ...)`` function in
its own module, and ``main()`` calls those builders instead of inlining the
argument definitions.

Handlers (the ``cmd_*`` functions) still live in ``main.py`` for now and are
dependency-injected into the builders so these modules never import ``main``
(which would create a cycle). Shared parser helpers live in
``_shared.py``.

Part of the god-file decomposition plan (Phase 2).
"""

from __future__ import annotations
