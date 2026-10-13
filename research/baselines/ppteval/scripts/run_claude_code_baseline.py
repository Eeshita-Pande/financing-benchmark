"""Run PPT-Eval's own CLI-agent harness (``ppteval.run_benchmark``) with Claude
Code as the agent under test and the local ``claude`` CLI as the VLM judge.

Usage (from the ppteval checkout root, inside its venv):

    CLAUDE_JUDGE_LOG=/path/judge.jsonl python /path/to/run_claude_code_baseline.py \
        --agent-config ppteval/configs/claude-code.yaml \
        --task-ids 3-007,Obesity-020 --results-dir results/claude-code-hard \
        [--task-registry task_registry] [--no-bypass]

Everything after the wrapper's own flags is forwarded to ``ppteval.run_benchmark``.
The wrapper:
  * patches ``ppteval.verify.ppt.verifier.vlm_call/llm_call`` with the Claude judge,
  * forces ``--conversion-mode libreoffice+poppler`` (no PowerPoint Online / COM here),
  * with ``--no-bypass`` replaces Claude Code's ``--dangerously-skip-permissions`` by
    ``--permission-mode acceptEdits --allowedTools <workspace tools>`` so the agent
    still runs unattended without the global bypass flag.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_judge  # noqa: E402

import ppteval.verify.ppt.verifier as _verifier  # noqa: E402
import rubric.utils.llm_tools as _llm_tools  # noqa: E402

_verifier.vlm_call = claude_judge.vlm_call
_verifier.llm_call = claude_judge.llm_call
_llm_tools.vlm_call = claude_judge.vlm_call
_llm_tools.llm_call = claude_judge.llm_call

AGENT_ALLOWED_TOOLS = os.environ.get(
    "CLAUDE_AGENT_ALLOWED_TOOLS",
    "Bash,Read,Write,Edit,MultiEdit,Glob,Grep,LS,Skill,TodoWrite",
)


def _patch_no_bypass() -> None:
    from ppteval.agents.cli.claude_code import ClaudeCodeAgent

    orig = ClaudeCodeAgent._build_command

    def _build_command(self, prompt, workspace_dir):
        cmd = orig(self, prompt, workspace_dir)
        cmd = [c for c in cmd if c != "--dangerously-skip-permissions"]
        cmd += ["--permission-mode", "acceptEdits", "--allowedTools", AGENT_ALLOWED_TOOLS]
        return cmd

    ClaudeCodeAgent._build_command = _build_command


def main() -> None:
    argv = sys.argv[1:]
    if "--no-bypass" in argv:
        argv.remove("--no-bypass")
        _patch_no_bypass()
    if "--conversion-mode" not in argv:
        argv += ["--conversion-mode", "libreoffice+poppler"]
    from ppteval.run_benchmark import main as rb_main

    sys.argv = ["ppteval.run_benchmark", *argv]
    rb_main()


if __name__ == "__main__":
    main()
