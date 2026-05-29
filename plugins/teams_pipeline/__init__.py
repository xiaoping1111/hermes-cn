"""Teams会议流水线插件

【产品经理理解要点】
Microsoft Teams会议自动化流水线插件，自动加入会议、转录内容、生成摘要并投递到指定频道。仅注册运维CLI命令。
- 核心能力：会议自动转录、AI摘要生成、定时排程、Graph订阅管理
- 使用方式：通过CLI命令操作(hermes teams-pipeline)，Agent通过terminal工具调用
"""

from __future__ import annotations

from plugins.teams_pipeline.cli import register_cli, teams_pipeline_command


def register(ctx) -> None:
    ctx.register_cli_command(
        name="teams-pipeline",
        help="Inspect and operate the Microsoft Teams meeting pipeline",
        setup_fn=register_cli,
        handler_fn=teams_pipeline_command,
        description=(
            "Operator CLI for the Microsoft Teams meeting pipeline. "
            "Lists jobs, inspects stored runs, replays jobs, validates Graph "
            "setup, and maintains Graph subscriptions."
        ),
    )
