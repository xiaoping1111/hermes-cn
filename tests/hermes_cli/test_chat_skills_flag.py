"""命令行界面测试 - chat·技能系统·flag

【产品经理理解要点】
验证命令行界面的技能系统功能
- 验证的功能: 聊天技能标志开关
- 核心测试场景: top level skills flag defaults to chat、chat subcommand accepts skills flag、chat subcommand accepts image flag 等共4个场景
- 业务影响: CLI命令可能出现异常，影响用户配置和操作体验

─────────────────────────────────────────────────────────────────
命令行界面测试 - chat·技能系统·flag

测试CLI命令处理与配置管理中chat相关的skills相关的flag功能
"""

import sys


def test_top_level_skills_flag_defaults_to_chat(monkeypatch):
    import hermes_cli.main as main_mod

    captured = {}

    def fake_cmd_chat(args):
        captured["skills"] = args.skills
        captured["command"] = args.command

    monkeypatch.setattr(main_mod, "cmd_chat", fake_cmd_chat)
    monkeypatch.setattr(
        sys,
        "argv",
        ["hermes", "-s", "hermes-agent-dev,github-auth"],
    )

    main_mod.main()

    assert captured == {
        "skills": ["hermes-agent-dev,github-auth"],
        "command": None,
    }


def test_chat_subcommand_accepts_skills_flag(monkeypatch):
    import hermes_cli.main as main_mod

    captured = {}

    def fake_cmd_chat(args):
        captured["skills"] = args.skills
        captured["query"] = args.query

    monkeypatch.setattr(main_mod, "cmd_chat", fake_cmd_chat)
    monkeypatch.setattr(
        sys,
        "argv",
        ["hermes", "chat", "-s", "github-auth", "-q", "hello"],
    )

    main_mod.main()

    assert captured == {
        "skills": ["github-auth"],
        "query": "hello",
    }


def test_chat_subcommand_accepts_image_flag(monkeypatch):
    import hermes_cli.main as main_mod

    captured = {}

    def fake_cmd_chat(args):
        captured["query"] = args.query
        captured["image"] = args.image

    monkeypatch.setattr(main_mod, "cmd_chat", fake_cmd_chat)
    monkeypatch.setattr(
        sys,
        "argv",
        ["hermes", "chat", "-q", "hello", "--image", "~/storage/shared/Pictures/cat.png"],
    )

    main_mod.main()

    assert captured == {
        "query": "hello",
        "image": "~/storage/shared/Pictures/cat.png",
    }


def test_continue_worktree_and_skills_flags_work_together(monkeypatch):
    import hermes_cli.main as main_mod

    captured = {}

    def fake_cmd_chat(args):
        captured["continue_last"] = args.continue_last
        captured["worktree"] = args.worktree
        captured["skills"] = args.skills
        captured["command"] = args.command

    monkeypatch.setattr(main_mod, "cmd_chat", fake_cmd_chat)
    monkeypatch.setattr(
        sys,
        "argv",
        ["hermes", "-c", "-w", "-s", "hermes-agent-dev"],
    )

    main_mod.main()

    assert captured == {
        "continue_last": True,
        "worktree": True,
        "skills": ["hermes-agent-dev"],
        "command": "chat",
    }
