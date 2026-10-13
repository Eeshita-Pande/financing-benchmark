"""Drop-in replacements for ai-rubric's ``vlm_call`` / ``llm_call`` that route
through the local Claude Code CLI (``claude -p``) instead of litellm.

Why: the ppteval verifier scores VLM rubric nodes through
``rubric.utils.llm_tools.vlm_call`` which needs ``RUBRIC_DEFAULT_LLM`` plus an
API key. This environment has neither, but it has an authenticated ``claude``
CLI. The CLI is invoked with only the ``Read`` tool allowed (so it can view the
rendered slide images) and asked to answer the rubric's grading prompt.

Every call is appended to the JSONL file named by ``CLAUDE_JUDGE_LOG`` so the
judgements are auditable. Scores produced through this path must be labelled
"Claude-judged" in any write-up: they are not the paper's judge model.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Union

JUDGE_TIMEOUT_S = int(os.environ.get("CLAUDE_JUDGE_TIMEOUT_S", "600"))
JUDGE_MODEL = os.environ.get("CLAUDE_JUDGE_MODEL")  # None -> CLI default
LOG_PATH = os.environ.get("CLAUDE_JUDGE_LOG")
_TMP = Path(tempfile.mkdtemp(prefix="claude_judge_imgs_"))


def _materialize(images: List[Union[str, bytes]]) -> list[str]:
    paths: list[str] = []
    for i, img in enumerate(images):
        if isinstance(img, (bytes, bytearray)):
            data = bytes(img)
        elif isinstance(img, str) and os.path.exists(img):
            paths.append(str(Path(img).resolve()))
            continue
        elif isinstance(img, str):
            data = base64.b64decode(img)
        else:
            raise TypeError(f"unsupported image type: {type(img)}")
        p = _TMP / f"img_{hashlib.sha1(data).hexdigest()[:12]}_{i}.png"
        p.write_bytes(data)
        paths.append(str(p))
    return paths


def _log(record: dict) -> None:
    if not LOG_PATH:
        return
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _run_claude(prompt: str, allowed_tools: str, add_dirs: list[str], max_turns: int) -> tuple[str, dict]:
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--max-turns", str(max_turns)]
    if allowed_tools:
        cmd += ["--allowedTools", allowed_tools]
    else:
        cmd += ["--allowedTools", "", "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Agent"]
    for d in add_dirs:
        cmd += ["--add-dir", d]
    if JUDGE_MODEL:
        cmd += ["--model", JUDGE_MODEL]
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=JUDGE_TIMEOUT_S, env=env, cwd=str(_TMP))
    dur = time.time() - t0
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"claude -p returned unparseable output (exit {proc.returncode}): {proc.stderr[-500:]}") from e
    if data.get("is_error"):
        raise RuntimeError(f"claude -p error: {data.get('result')}")
    meta = {
        "duration_s": round(dur, 1),
        "num_turns": data.get("num_turns"),
        "cost_usd": data.get("total_cost_usd"),
        "models": sorted((data.get("modelUsage") or {}).keys()),
        "exit_code": proc.returncode,
    }
    return str(data.get("result") or ""), meta


def vlm_call(prompt: str, images: List[Union[str, bytes]], temperature: float = 0.7, max_tokens: int | None = None) -> str:
    paths = _materialize(images)
    listing = "\n".join(f"{i + 1}. {p}" for i, p in enumerate(paths))
    full = (
        "You are acting as the vision-language grading model for a PowerPoint editing benchmark. "
        "First use the Read tool to view EACH of the following image files, in order "
        "(image 1 is listed first; when two images are given, image 1 is the ORIGINAL slide and image 2 is the MODIFIED slide "
        "unless the grading prompt says otherwise):\n"
        f"{listing}\n\n"
        "Then answer the grading prompt below strictly in the format it asks for. "
        "Reply with only your answer (no preamble, no questions back).\n\n"
        f"<grading_prompt>\n{prompt}\n</grading_prompt>"
    )
    add_dirs = sorted({str(Path(p).parent) for p in paths})
    result, meta = _run_claude(full, "Read", add_dirs, max_turns=len(paths) + 6)
    _log({"kind": "vlm", "prompt": prompt, "images": paths, "response": result, **meta})
    return result


def llm_call(prompt: str, temperature: float = 0.7, max_tokens: int | None = None) -> str:
    full = (
        "You are acting as the text grading model for a PowerPoint editing benchmark. "
        "Answer the grading prompt below strictly in the format it asks for. Reply with only your answer.\n\n"
        f"<grading_prompt>\n{prompt}\n</grading_prompt>"
    )
    result, meta = _run_claude(full, "", [], max_turns=2)
    _log({"kind": "llm", "prompt": prompt, "response": result, **meta})
    return result
