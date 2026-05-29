"""TUI斜杠命令工作进程

【产品经理理解要点】
为TUI中的斜杠命令（如/model、/tools）提供持久化的命令执行环境。
- 核心职责：维护一个常驻的HermesCLI子进程，复用会话状态执行斜杠命令
- 通信协议：通过stdin/stdout传递JSON格式的命令和结果
- 设计原因：斜杠命令需要完整的CLI上下文（如模型列表、会话历史），直接子进程复用比每次重建更高效

─────────────────────────────────────────────────────────────────
Persistent slash-command worker — one HermesCLI per TUI session.

Protocol: reads JSON lines from stdin {id, command}, writes {id, ok, output|error} to stdout.
"""

import argparse
import contextlib
import io
import json
import os
import sys

import cli as cli_mod
from cli import HermesCLI
from rich.console import Console


def _run(cli: HermesCLI, command: str) -> str:
    cmd = (command or "").strip()
    if not cmd:
        return ""
    if not cmd.startswith("/"):
        cmd = f"/{cmd}"

    buf = io.StringIO()

    # Rich Console captures its file handle at construction time, so
    # contextlib.redirect_stdout won't affect it. Swap the console's
    # underlying file to our buffer so self.console.print() is captured.
    cli.console = Console(file=buf, force_terminal=True, width=120)

    old = getattr(cli_mod, "_cprint", None)
    if old is not None:
        cli_mod._cprint = lambda text: print(text)

    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            cli.process_command(cmd)
    finally:
        if old is not None:
            cli_mod._cprint = old

    return buf.getvalue().rstrip()


def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--session-key", required=True)
    p.add_argument("--model", default="")
    args = p.parse_args()

    os.environ["HERMES_SESSION_KEY"] = args.session_key
    os.environ["HERMES_INTERACTIVE"] = "1"

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        cli = HermesCLI(model=args.model or None, compact=True, resume=args.session_key, verbose=False)

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        rid = None
        try:
            req = json.loads(line)
            rid = req.get("id")
            out = _run(cli, req.get("command", ""))
            sys.stdout.write(json.dumps({"id": rid, "ok": True, "output": out}) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"id": rid, "ok": False, "error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
