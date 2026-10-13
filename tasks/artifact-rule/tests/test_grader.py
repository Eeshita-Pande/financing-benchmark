#!/usr/bin/env python3
"""Run the grader on the hand-made fixtures and assert the expected verdicts.

Usage: python3 tests/test_grader.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import grade  # noqa: E402

INSTANCES = ["i1_case4", "i2_schedule", "i3_sensitivity",
             "i2b_schedule_first", "i4_sensitivity_anchor", "i5_sensitivity_notes_anchor", "i6_sensitivity_scale"]


def main():
    failures = 0
    for inst in INSTANCES:
        inst_dir = os.path.join(ROOT, "instances", inst)
        # untouched input must fail (no new slide)
        r0 = grade.grade(os.path.join(inst_dir, "inputs", "ic_deck_base.pptx"), inst_dir)
        ok0 = not r0["strict_pass"] and not r0["checks"]["new_slide_present"]["pass"]
        # correct fixture must pass every check
        rc = grade.grade(os.path.join(HERE, "fixtures", f"{inst}_correct.pptx"), inst_dir)
        okc = rc["strict_pass"]
        # misplaced fixture must fail title_order (and agenda order for i1) and nothing else
        rm = grade.grade(os.path.join(HERE, "fixtures", f"{inst}_misplaced.pptx"), inst_dir)
        failed = sorted(k for k, v in rm["checks"].items() if not v["pass"])
        expect_failed = ["title_order"]
        okm = (not rm["strict_pass"]) and failed == expect_failed \
            and rm["checks"]["title_order"]["detail"]["matches_literal_placement"]
        verdicts = [("untouched", ok0, r0), ("correct", okc, rc), ("misplaced", okm, rm)]
        decoy_path = os.path.join(HERE, "fixtures", f"{inst}_decoy.pptx")
        if os.path.exists(decoy_path):
            # decoy fixture (e.g. workbook tab order for i2b) must fail title_order only and be flagged as decoy
            rd = grade.grade(decoy_path, inst_dir)
            failed_d = sorted(k for k, v in rd["checks"].items() if not v["pass"])
            okd = (not rd["strict_pass"]) and failed_d == ["title_order"] \
                and rd["checks"]["title_order"]["detail"]["matches_decoy_placement"] is True \
                and not rd["checks"]["title_order"]["detail"]["matches_literal_placement"]
            verdicts.append(("decoy", okd, rd))
        for tag, ok, r in verdicts:
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {inst} {tag}: strict={r['strict_pass']} failed_checks="
                  f"{[k for k, v in r['checks'].items() if not v['pass']]}")
            if not ok:
                failures += 1
                print(json.dumps(r["checks"], indent=1, ensure_ascii=False)[:3000])
    # CLI exit code contract
    p = subprocess.run([sys.executable, os.path.join(ROOT, "grade.py"),
                        os.path.join(HERE, "fixtures", "i1_case4_correct.pptx"),
                        os.path.join(ROOT, "instances", "i1_case4")], capture_output=True, text=True)
    cli_ok = p.returncode == 0 and json.loads(p.stdout)["strict_pass"] is True
    print(f"[{'PASS' if cli_ok else 'FAIL'}] grade.py CLI exit code / JSON output")
    failures += 0 if cli_ok else 1
    print("ALL TESTS PASSED" if failures == 0 else f"{failures} TEST(S) FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
