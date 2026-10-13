#!/usr/bin/env python3
"""Deterministic grader for the artifact-rule task.

Usage: python3 grade.py <output.pptx> <instance_dir>

<instance_dir> must contain inputs/ic_deck_base.pptx and expected/spec.json.
Prints JSON: {"checks": {name: {"pass": bool, "detail": ...}}, "strict_pass": bool, ...}.
No workbook calculation is involved: expected values are stored in expected/spec.json.
"""
import json
import os
import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

DASHES = {"—": "-", "–": "-", "−": "-", "‐": "-", "‑": "-"}


def norm(s):
    s = s or ""
    for k, v in DASHES.items():
        s = s.replace(k, v)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def alnum(s):
    return re.sub(r"[^a-z0-9%]+", "", norm(s).lower())


def shape_text(shape):
    if shape.has_text_frame:
        return shape.text_frame.text
    if getattr(shape, "has_table", False) and shape.has_table:
        return "\n".join("|".join(c.text for c in row.cells) for row in shape.table.rows)
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        return "\n".join(shape_text(s) for s in shape.shapes)
    return ""


def slide_title(slide):
    t = slide.shapes.title
    if t is not None and t.has_text_frame:
        return t.text_frame.text
    # fall back: first text shape
    for s in slide.shapes:
        if s.has_text_frame and s.text_frame.text.strip():
            return s.text_frame.text
    return ""


def notes_text(slide):
    if not slide.has_notes_slide:
        return ""
    return slide.notes_slide.notes_text_frame.text


def picture_count(slide):
    n = 0
    for s in slide.shapes:
        if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
            n += 1
    return n


def structure_sig(slide):
    sig = []
    for s in slide.shapes:
        ph = None
        if s.is_placeholder:
            ph = str(s.placeholder_format.type)
        dims = None
        if getattr(s, "has_table", False) and s.has_table:
            dims = (len(s.table.rows), len(s.table.columns))
        sig.append((str(s.shape_type), ph, dims))
    return sorted(sig, key=repr)


def slide_snapshot(slide):
    return {
        "title": norm(slide_title(slide)),
        "layout": slide.slide_layout.name,
        "shape_count": len(slide.shapes),
        "texts": [norm(shape_text(s)) for s in slide.shapes],
        "notes": norm(notes_text(slide)),
        "pictures": picture_count(slide),
    }


NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


def numbers_in(text):
    text = norm(text)
    out = []
    for m in NUM_RE.findall(text):
        try:
            out.append(float(m.replace(",", "")))
        except ValueError:
            pass
    return out


def value_present(expected, text):
    """True if the expected workbook value appears in text (lenient on unit scaling)."""
    if isinstance(expected, str):
        return alnum(expected) in alnum(text)
    nums = numbers_in(text)
    candidates = [expected]
    if expected != 0:
        candidates += [expected / 1000.0, expected * 1000.0, expected / 100.0, expected * 100.0]
    for n in nums:
        for c in candidates:
            if abs(n - c) < 0.006:
                return True
    return False


def find_slide(prs, title):
    for i, s in enumerate(prs.slides):
        if norm(slide_title(s)) == norm(title):
            return i, s
    return None, None


def find_table(slide):
    for s in slide.shapes:
        if getattr(s, "has_table", False) and s.has_table:
            return s.table
    return None


def grade(output_path, instance_dir):
    spec = json.load(open(os.path.join(instance_dir, "expected", "spec.json")))
    inp = Presentation(os.path.join(instance_dir, "inputs", "ic_deck_base.pptx"))
    checks = {}

    def add(name, ok, detail=None):
        checks[name] = {"pass": bool(ok), "detail": detail}

    try:
        out = Presentation(output_path)
    except Exception as e:  # noqa: BLE001
        add("file_opens", False, f"{type(e).__name__}: {e}")
        return finish(checks, spec, None)
    add("file_opens", True)

    in_snaps = [slide_snapshot(s) for s in inp.slides]
    out_snaps = [slide_snapshot(s) for s in out.slides]
    in_titles = [s["title"] for s in in_snaps]
    out_titles = [s["title"] for s in out_snaps]
    exp_titles = [norm(t) for t in spec["expected_title_order"]]
    lit_titles = [norm(t) for t in spec["literal_placement_title_order"]]
    new_title = norm(spec["new_slide_title"])

    # 1. slide count and title order
    add("slide_count", len(out_titles) == len(in_titles) + 1, {"input": len(in_titles), "output": len(out_titles)})
    add("new_slide_present", out_titles.count(new_title) == 1, {"count": out_titles.count(new_title)})
    add("title_order", out_titles == exp_titles,
        {"output": out_titles, "expected": exp_titles,
         "matches_literal_placement": out_titles == lit_titles,
         "new_slide_index": out_titles.index(new_title) if new_title in out_titles else None,
         "expected_index": spec["expected_new_slide_index"]})
    # 1b. relative order of the pre-existing slides preserved (diagnostic)
    remaining = [t for t in out_titles if t != new_title]
    add("existing_slides_order_preserved", remaining == in_titles)

    # 2. new slide structure vs template
    ni, new_slide = find_slide(out, new_title)
    ti, tmpl_in = find_slide(inp, spec["structure_template_title"])
    if new_slide is None:
        add("new_slide_structure", False, "new slide not found")
        add("new_slide_values", False, "new slide not found")
        add("new_slide_no_placeholders_left", False, "new slide not found")
    else:
        same_layout = new_slide.slide_layout.name == tmpl_in.slide_layout.name
        same_count = len(new_slide.shapes) == len(tmpl_in.shapes)
        same_sig = structure_sig(new_slide) == structure_sig(tmpl_in)
        add("new_slide_structure", same_layout and same_count and same_sig,
            {"layout": new_slide.slide_layout.name, "template_layout": tmpl_in.slide_layout.name,
             "shape_count": len(new_slide.shapes), "template_shape_count": len(tmpl_in.shapes),
             "signature_match": same_sig})
        # 3. values
        vals = spec["values"]
        details = {}
        ok = True
        if vals["kind"] == "card":
            texts = [norm(shape_text(s)) for s in new_slide.shapes]
            for tile in vals["tiles"]:
                hits = [t for t in texts if alnum(tile["label"]) in alnum(t) and t != norm(slide_title(new_slide))]
                # a tile is a non-table shape whose text carries the label
                found = any(value_present(tile["value"], t) for t in hits)
                details[tile["label"]] = {"pass": found, "texts": hits[:3]}
                ok = ok and found
            tbl = find_table(new_slide)
            if tbl is None:
                ok = False
                details["table"] = "no table on new slide"
            else:
                for row in vals["table_rows"]:
                    found = False
                    seen = None
                    for r in tbl.rows:
                        cells = [c.text for c in r.cells]
                        if cells and alnum(row["label"]) in alnum(cells[0]):
                            seen = cells
                            found = any(value_present(row["value"], c) for c in cells[1:])
                            break
                    details[row["label"]] = {"pass": found, "row": seen}
                    ok = ok and found
        else:  # schedule
            tbl = find_table(new_slide)
            if tbl is None:
                ok = False
                details["table"] = "no table on new slide"
            else:
                hdr = [c.text for c in tbl.rows[0].cells]
                hdr_ok = [alnum(h) for h in hdr] == [alnum(h) for h in vals["header"]]
                details["header"] = {"pass": hdr_ok, "row": hdr}
                ok = ok and hdr_ok
                for exp_row in vals["rows"]:
                    found = False
                    seen = None
                    for r in list(tbl.rows)[1:]:
                        cells = [c.text for c in r.cells]
                        if cells and alnum(exp_row[0]) == alnum(cells[0]):
                            seen = cells
                            found = len(cells) == len(exp_row) and all(
                                value_present(exp_row[j], cells[j]) for j in range(1, len(exp_row)))
                            break
                    details[exp_row[0]] = {"pass": found, "row": seen}
                    ok = ok and found
                # row order must follow the workbook
                labels = [alnum(r.cells[0].text) for r in list(tbl.rows)[1:]]
                order_ok = labels == [alnum(r[0]) for r in vals["rows"]]
                details["row_order"] = {"pass": order_ok, "rows": labels}
                ok = ok and order_ok
        add("new_slide_values", ok, details)
        alltext = " ".join(norm(shape_text(s)) for s in new_slide.shapes)
        leftovers = [t for t in spec["forbidden_text_on_new_slide"] if alnum(t) in alnum(alltext)]
        add("new_slide_no_placeholders_left", not leftovers, {"leftover": leftovers})

    # 4. reference slide unchanged
    ri_in, ref_in = find_slide(inp, spec["reference_title"])
    ri_out, ref_out = find_slide(out, spec["reference_title"])
    if ref_out is None:
        add("reference_unchanged", False, "reference slide missing")
    else:
        a, b = slide_snapshot(ref_in), slide_snapshot(ref_out)
        diffs = {k: {"input": a[k], "output": b[k]} for k in a if a[k] != b[k]}
        add("reference_unchanged", not diffs, diffs or None)

    # 5. agenda
    agenda_spec = spec.get("agenda_check")
    if agenda_spec:
        _, ag_in = find_slide(inp, "Agenda")
        _, ag_out = find_slide(out, "Agenda")
        if ag_out is None:
            add("agenda_updated", False, "agenda slide missing")
        else:
            text = " ".join(norm(shape_text(s)) for s in ag_out.shapes)
            contains = all(norm(m) in text for m in agenda_spec["must_contain"])
            positions = []
            for lab in agenda_spec["case_labels_order"]:
                positions.append(text.find(lab))
            all_present = all(p >= 0 for p in positions)
            order_ok = all_present and positions == sorted(positions)
            # original agenda lines preserved
            orig_lines = []
            for s in ag_in.shapes:
                if s.has_text_frame:
                    orig_lines += [norm(p.text) for p in s.text_frame.paragraphs if norm(p.text)]
            kept = [l for l in orig_lines if l in text]
            preserved = len(kept) == len(orig_lines)
            add("agenda_updated", contains and all_present and order_ok and preserved,
                {"mentions_new_case": contains, "case_order_positions": positions, "order_ok": order_ok,
                 "original_lines_preserved": preserved,
                 "missing_original_lines": [l for l in orig_lines if l not in text]})

    # 6. all other slides unchanged
    allowed = {norm(t) for t in spec["slides_allowed_to_change"]} | {norm(spec["reference_title"])}
    changed = {}
    missing = []
    for snap in in_snaps:
        if snap["title"] in allowed:
            continue
        match = [o for o in out_snaps if o["title"] == snap["title"]]
        if not match:
            missing.append(snap["title"])
            continue
        o = match[0]
        diffs = {k: {"input": snap[k], "output": o[k]} for k in snap if snap[k] != o[k]}
        if diffs:
            changed[snap["title"]] = diffs
    add("other_slides_unchanged", not changed and not missing,
        {"changed": changed, "missing": missing} if (changed or missing) else None)

    return finish(checks, spec, out_titles)


def finish(checks, spec, out_titles):
    strict = all(c["pass"] for c in checks.values())
    placement_ok = checks.get("title_order", {}).get("pass", False)
    non_placement = {k: v["pass"] for k, v in checks.items() if k not in ("title_order", "agenda_updated")}
    return {
        "instance": spec["instance"],
        "strict_pass": strict,
        "placement_pass": placement_ok,
        "all_non_placement_pass": all(non_placement.values()),
        "checks": checks,
        "output_title_order": out_titles,
    }


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    result = grade(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["strict_pass"] else 1)


if __name__ == "__main__":
    main()
