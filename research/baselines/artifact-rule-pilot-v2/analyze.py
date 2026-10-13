#!/usr/bin/env python3
"""Aggregate run.json records into results.json (per instance x condition x model) with per-check rates.

v2: also counts decoy placements (workbook tab order, I2b), notes reads, and lists every failed run with the
signals needed to classify it (rule seen in a tool result, rule quoted by the agent, thumbnails rendered,
position chosen).
Usage: python3 analyze.py RUNS_DIR results.json
"""
import glob
import json
import os
import sys
from collections import defaultdict

runs_dir = sys.argv[1]
out_path = sys.argv[2]
records = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(runs_dir, "*", "run.json")))]


def model_label(r):
    ms = [m for m in (r.get("models_used") or []) if "haiku" not in m]
    return ms[0] if ms else (r["requested_model"] if r["requested_model"] != "default" else "unknown")


def title_detail(r):
    return (r["grade"].get("checks", {}).get("title_order", {}).get("detail") or {})


def position_label(r):
    d = title_detail(r)
    if r["grade"].get("placement_pass"):
        return "expected"
    if d.get("matches_literal_placement"):
        return "literal default (appended to block)"
    if d.get("matches_decoy_placement"):
        return "decoy (workbook tab order)"
    idx = d.get("new_slide_index")
    out = d.get("output") or []
    if idx is None:
        return "new slide missing"
    prev = out[idx - 1] if idx > 0 else "(start)"
    return f"other: index {idx}, after '{prev}'"


groups = defaultdict(list)
for r in records:
    groups[(r["instance"], r["condition"], model_label(r))].append(r)

ORDER = {"i2b_schedule_first": 0, "i4_sensitivity_anchor": 1, "i5_sensitivity_notes_anchor": 2, "i6_sensitivity_scale": 3}
summary = []
for (inst, cond, model), rs in sorted(groups.items(), key=lambda kv: (ORDER.get(kv[0][0], 9), kv[0][1], kv[0][2])):
    n = len(rs)
    strict = sum(1 for r in rs if r["grade"]["strict_pass"])
    placement = sum(1 for r in rs if r["grade"].get("placement_pass"))
    nonplace = sum(1 for r in rs if r["grade"].get("all_non_placement_pass"))
    literal = sum(1 for r in rs if title_detail(r).get("matches_literal_placement"))
    decoy = sum(1 for r in rs if title_detail(r).get("matches_decoy_placement"))
    check_names = sorted({c for r in rs for c in r["grade"].get("checks", {})})
    per_check = {c: sum(1 for r in rs if r["grade"].get("checks", {}).get(c, {}).get("pass")) for c in check_names}
    runs = []
    for r in rs:
        t = r["transcript"]
        failed = [c for c, v in r["grade"].get("checks", {}).items() if not v["pass"]]
        runs.append({
            "tag": r["tag"], "strict_pass": r["grade"]["strict_pass"], "failed_checks": failed,
            "position": position_label(r),
            "new_slide_index": title_detail(r).get("new_slide_index"),
            "expected_index": title_detail(r).get("expected_index"),
            "models_used": r.get("models_used"), "wall_seconds": r["wall_seconds"], "timed_out": r["timed_out"],
            "returncode": r.get("returncode"),
            "tool_calls": t.get("tool_calls"), "tools": t.get("tools"),
            "rule_seen_in_tool_output": t.get("rule_seen_in_tool_output"),
            "rule_quoted_by_agent": t.get("rule_quoted_by_agent"),
            "rendered_thumbnails": t.get("rendered_thumbnails"), "read_notes": t.get("read_notes"),
            "cost_usd": (t.get("result") or {}).get("total_cost_usd"),
            "num_turns": (t.get("result") or {}).get("num_turns"),
            "final_text": (t.get("final_text") or "")[:1500],
        })
    summary.append({
        "instance": inst, "condition": cond, "model": model, "n": n,
        "strict_pass": strict, "strict_pass_rate": round(strict / n, 3) if n else None,
        "placement_pass": placement, "all_non_placement_pass": nonplace,
        "literal_default_placement": literal, "decoy_placement": decoy,
        "per_check_pass": per_check,
        "rule_seen_in_tool_output": sum(1 for r in rs if r["transcript"].get("rule_seen_in_tool_output")),
        "rule_quoted_by_agent": sum(1 for r in rs if r["transcript"].get("rule_quoted_by_agent")),
        "read_notes": sum(1 for r in rs if r["transcript"].get("read_notes")),
        "rendered_thumbnails": sum(1 for r in rs if r["transcript"].get("rendered_thumbnails")),
        "timed_out": sum(1 for r in rs if r["timed_out"]),
        "mean_wall_seconds": round(sum(r["wall_seconds"] for r in rs) / n, 1) if n else None,
        "total_cost_usd": round(sum((r["transcript"].get("result") or {}).get("total_cost_usd") or 0 for r in rs), 2),
        "runs": runs,
        "failed_runs": [x for x in runs if not x["strict_pass"]],
    })

total_cost = round(sum(g["total_cost_usd"] for g in summary), 2)
total_wall = round(sum(r["wall_seconds"] for r in records) / 60, 1)
json.dump({"total_runs": len(records), "total_cost_usd": total_cost, "total_wall_minutes": total_wall,
           "groups": summary}, open(out_path, "w"), indent=2, ensure_ascii=False)
print(f"{len(records)} runs, USD {total_cost}, {total_wall} min")
print(f"{'instance':28} {'cond':9} {'model':18} {'n':>2} {'strict':>6} {'place':>5} {'nonpl':>5} {'literal':>7} {'decoy':>5} {'seen':>4} {'quoted':>6} {'notes':>5} {'thumbs':>6}")
for g in summary:
    print(f"{g['instance']:28} {g['condition']:9} {g['model']:18} {g['n']:>2} {g['strict_pass']:>6} {g['placement_pass']:>5} "
          f"{g['all_non_placement_pass']:>5} {g['literal_default_placement']:>7} {g['decoy_placement']:>5} "
          f"{g['rule_seen_in_tool_output']:>4} {g['rule_quoted_by_agent']:>6} {g['read_notes']:>5} {g['rendered_thumbnails']:>6}")
