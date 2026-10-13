#!/usr/bin/env python3
"""Aggregate run.json records into results.json (per instance x condition x model) with per-check rates."""
import glob
import json
import os
import sys
from collections import defaultdict

runs_dir = sys.argv[1]
out_path = sys.argv[2]
records = []
for p in sorted(glob.glob(os.path.join(runs_dir, "*", "run.json"))):
    records.append(json.load(open(p)))


def model_label(r):
    ms = [m for m in (r.get("models_used") or []) if "haiku" not in m]
    return ms[0] if ms else (r["requested_model"] if r["requested_model"] != "default" else "unknown")


groups = defaultdict(list)
for r in records:
    groups[(r["instance"], r["condition"], model_label(r))].append(r)

summary = []
for (inst, cond, model), rs in sorted(groups.items()):
    n = len(rs)
    strict = sum(1 for r in rs if r["grade"]["strict_pass"])
    placement = sum(1 for r in rs if r["grade"].get("placement_pass"))
    nonplace = sum(1 for r in rs if r["grade"].get("all_non_placement_pass"))
    literal = sum(1 for r in rs if (r["grade"].get("checks", {}).get("title_order", {}).get("detail") or {})
                  .get("matches_literal_placement"))
    check_names = sorted({c for r in rs for c in r["grade"].get("checks", {})})
    per_check = {c: sum(1 for r in rs if r["grade"].get("checks", {}).get(c, {}).get("pass")) for c in check_names}
    runs = []
    for r in rs:
        t = r["transcript"]
        failed = [c for c, v in r["grade"].get("checks", {}).items() if not v["pass"]]
        runs.append({
            "tag": r["tag"], "strict_pass": r["grade"]["strict_pass"], "failed_checks": failed,
            "new_slide_index": (r["grade"].get("checks", {}).get("title_order", {}).get("detail") or {}).get("new_slide_index"),
            "matches_literal_placement": (r["grade"].get("checks", {}).get("title_order", {}).get("detail") or {}).get("matches_literal_placement"),
            "models_used": r.get("models_used"), "wall_seconds": r["wall_seconds"], "timed_out": r["timed_out"],
            "tool_calls": t.get("tool_calls"), "tools": t.get("tools"),
            "rule_seen_in_tool_output": t.get("rule_seen_in_tool_output"),
            "rule_quoted_by_agent": t.get("rule_quoted_by_agent"),
            "rendered_thumbnails": t.get("rendered_thumbnails"), "read_notes": t.get("read_notes"),
            "cost_usd": (t.get("result") or {}).get("total_cost_usd"),
            "num_turns": (t.get("result") or {}).get("num_turns"),
            "final_text": (t.get("final_text") or "")[:1200],
        })
    summary.append({
        "instance": inst, "condition": cond, "model": model, "n": n,
        "strict_pass": strict, "strict_pass_rate": round(strict / n, 3) if n else None,
        "placement_pass": placement, "all_non_placement_pass": nonplace,
        "literal_default_placement": literal,
        "per_check_pass": per_check,
        "rule_seen_in_tool_output": sum(1 for r in rs if r["transcript"].get("rule_seen_in_tool_output")),
        "rendered_thumbnails": sum(1 for r in rs if r["transcript"].get("rendered_thumbnails")),
        "mean_wall_seconds": round(sum(r["wall_seconds"] for r in rs) / n, 1) if n else None,
        "runs": runs,
    })

json.dump({"total_runs": len(records), "groups": summary}, open(out_path, "w"), indent=2, ensure_ascii=False)
print(f"{'instance':16} {'cond':9} {'model':20} {'n':>2} {'strict':>6} {'place':>5} {'nonpl':>5} {'literal':>7} {'ruleSeen':>8} {'thumbs':>6}")
for g in summary:
    print(f"{g['instance']:16} {g['condition']:9} {g['model']:20} {g['n']:>2} {g['strict_pass']:>6} {g['placement_pass']:>5} "
          f"{g['all_non_placement_pass']:>5} {g['literal_default_placement']:>7} {g['rule_seen_in_tool_output']:>8} {g['rendered_thumbnails']:>6}")
