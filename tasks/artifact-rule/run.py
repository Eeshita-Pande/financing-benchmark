#!/usr/bin/env python3
"""Run the artifact-rule task against the Claude Code CLI and grade each run.

Each run gets a fresh working directory containing only brief.md and inputs/ (never expected/ or the
grader). The agent is told to edit inputs/ic_deck_base.pptx in place. The transcript is captured as
stream-json, the output is graded with grade.py, and a per-run JSON record is written.

Usage:
  python3 run.py --out RUNS_DIR [--instances i1_case4,i2_schedule,i3_sensitivity]
                 [--conditions artefact,control] [--runs 5] [--model MODEL] [--timeout 900]
Runs whose record already exists are skipped, so the matrix is resumable.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grade  # noqa: E402

INSTANCES = ["i1_case4", "i2_schedule", "i3_sensitivity",
             "i2b_schedule_first", "i4_sensitivity_anchor", "i5_sensitivity_notes_anchor", "i6_sensitivity_scale"]
CONDITIONS = {"artefact": "brief.md", "control": "brief_control.md", "anchor": "brief_anchor.md"}
PROMPT_TAIL = ("\n\nEdit inputs/ic_deck_base.pptx in place and keep the filename. Do not read or write "
               "anything outside this directory. When you are done, stop.")
ALLOWED_TOOLS = "Bash,Read,Write,Edit,Glob,Grep"
RENDER_RE = re.compile(r"soffice|libreoffice|pdftoppm|convert-to|thumbnail|\.png", re.I)


def child_env():
    env = dict(os.environ)
    # do not let the nested CLI attach itself to this orchestrating session
    for k in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_TEE_SDK_STDOUT", "CLAUDE_CODE_SYNC_SESSION_REFS",
              "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDECODE"):
        env.pop(k, None)
    return env


def content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif "content" in c:
                    parts.append(content_text(c["content"]))
            elif isinstance(c, str):
                parts.append(c)
        return "\n".join(parts)
    return ""


def analyse_transcript(path, rule_text):
    """Summarise what the agent did, from the stream-json transcript."""
    frag = grade.alnum(rule_text)[:60]
    info = {"events": 0, "tool_calls": 0, "tools": {}, "bash_commands": [], "rule_seen_in_tool_output": False,
            "rule_quoted_by_agent": False, "rendered_thumbnails": False, "read_notes": False,
            "assistant_text": [], "result": None}
    if not os.path.exists(path):
        return info
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            info["events"] += 1
            t = ev.get("type")
            if t == "assistant":
                for c in ev.get("message", {}).get("content", []):
                    if c.get("type") == "tool_use":
                        info["tool_calls"] += 1
                        name = c.get("name")
                        info["tools"][name] = info["tools"].get(name, 0) + 1
                        inp = c.get("input", {})
                        blob = json.dumps(inp)
                        if name == "Bash":
                            cmd = inp.get("command", "")
                            info["bash_commands"].append(cmd[:400])
                        if RENDER_RE.search(blob):
                            info["rendered_thumbnails"] = True
                        if "notes_slide" in blob or "notesSlide" in blob or "notes_text" in blob:
                            info["read_notes"] = True
                    elif c.get("type") == "text":
                        txt = c.get("text", "")
                        info["assistant_text"].append(txt[:2000])
                        if frag and frag in grade.alnum(txt):
                            info["rule_quoted_by_agent"] = True
            elif t == "user":
                for c in ev.get("message", {}).get("content", []):
                    if isinstance(c, dict) and c.get("type") == "tool_result":
                        txt = content_text(c.get("content"))
                        if frag and frag in grade.alnum(txt):
                            info["rule_seen_in_tool_output"] = True
            elif t == "result":
                info["result"] = {k: ev.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms",
                                                          "total_cost_usd", "stop_reason", "terminal_reason")}
                info["result"]["models"] = sorted((ev.get("modelUsage") or {}).keys())
                info["result"]["model_usage"] = {m: {k: v.get(k) for k in ("inputTokens", "outputTokens",
                                                                              "cacheReadInputTokens", "costUSD")}
                                                 for m, v in (ev.get("modelUsage") or {}).items()}
                info["final_text"] = (ev.get("result") or "")[:3000]
    return info


def one_run(task_dir, instance, condition, k, model, timeout, out_root):
    inst_dir = os.path.join(task_dir, "instances", instance)
    tag = f"{instance}__{condition}__{model or 'default'}__r{k}"
    run_dir = os.path.join(out_root, tag)
    record_path = os.path.join(run_dir, "run.json")
    if os.path.exists(record_path):
        print(f"[skip] {tag} already done", flush=True)
        return json.load(open(record_path))
    work = os.path.join(run_dir, "work")
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(work)
    shutil.copytree(os.path.join(inst_dir, "inputs"), os.path.join(work, "inputs"))
    brief = open(os.path.join(inst_dir, CONDITIONS[condition]), encoding="utf-8").read()
    with open(os.path.join(work, "brief.md"), "w", encoding="utf-8") as f:
        f.write(brief)
    prompt = brief + PROMPT_TAIL
    cmd = ["claude", "-p", prompt, "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED_TOOLS,
           "--output-format", "stream-json", "--verbose"]
    if model:
        cmd += ["--model", model]
    transcript = os.path.join(run_dir, "transcript.jsonl")
    stderr_path = os.path.join(run_dir, "stderr.txt")
    print(f"[start] {tag}", flush=True)
    t0 = time.time()
    timed_out = False
    with open(transcript, "w") as so, open(stderr_path, "w") as se:
        try:
            proc = subprocess.run(cmd, cwd=work, env=child_env(), stdout=so, stderr=se, timeout=timeout,
                                  stdin=subprocess.DEVNULL)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            rc = None
    wall = time.time() - t0
    out_pptx = os.path.join(work, "inputs", "ic_deck_base.pptx")
    spec = json.load(open(os.path.join(inst_dir, "expected", "spec.json")))
    if os.path.exists(out_pptx):
        try:
            g = grade.grade(out_pptx, inst_dir)
        except Exception as e:  # noqa: BLE001
            g = {"strict_pass": False, "error": f"{type(e).__name__}: {e}", "checks": {}}
    else:
        g = {"strict_pass": False, "error": "output deck missing", "checks": {}}
    shutil.copy(out_pptx, os.path.join(run_dir, "output.pptx")) if os.path.exists(out_pptx) else None
    # stray files the agent left in the workdir (diagnostic)
    stray = []
    for root, _, files in os.walk(work):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), work)
            if rel not in ("brief.md", "inputs/ic_deck_base.pptx", "inputs/model_outputs.xlsx"):
                stray.append(rel)
    analysis = analyse_transcript(transcript, spec["rule_text"])
    record = {
        "tag": tag, "instance": instance, "condition": condition, "requested_model": model or "default",
        "run_index": k, "returncode": rc, "timed_out": timed_out, "wall_seconds": round(wall, 1),
        "models_used": (analysis.get("result") or {}).get("models"),
        "grade": g, "transcript": analysis, "stray_files": stray[:50],
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
    }
    with open(os.path.join(run_dir, "grade.json"), "w") as f:
        json.dump(g, f, indent=2, ensure_ascii=False)
    with open(record_path, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    failed = [c for c, v in g.get("checks", {}).items() if not v["pass"]]
    print(f"[done] {tag} strict={g['strict_pass']} failed={failed} wall={wall:.0f}s "
          f"models={record['models_used']} timed_out={timed_out}", flush=True)
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--instances", default=",".join(INSTANCES))
    ap.add_argument("--conditions", default="artefact,control")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--model", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--task-dir", default=HERE)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    records = []
    for k in range(1, args.runs + 1):
        for instance in args.instances.split(","):
            for condition in args.conditions.split(","):
                records.append(one_run(args.task_dir, instance, condition, k, args.model, args.timeout, args.out))
    with open(os.path.join(args.out, f"index_{args.model or 'default'}_{int(time.time())}.json"), "w") as f:
        json.dump([{k: r[k] for k in ("tag", "instance", "condition", "requested_model", "run_index",
                                      "models_used", "timed_out")} | {"strict_pass": r["grade"]["strict_pass"]}
                   for r in records], f, indent=2)


if __name__ == "__main__":
    main()
