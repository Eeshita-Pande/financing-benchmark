# Artifact-rule task (PowerPoint only)

A deterministic deck-editing benchmark that targets one failure mode: an agent fills a new slide
correctly, duplicates the right layout, leaves the locked reference slide alone, and then puts the slide
where the brief *literally allows* instead of where a placement rule *inside the deck* requires.
Thumbnail self-checks pass because every slide looks right on its own. Only slide order is wrong.

Nothing here depends on a workbook calculation. The workbook is frozen, read-only reference data; the
expected values are stored in `expected/spec.json` and the grader compares text and structure only.

## The four ingredients

1. **An under-determined brief that is true under the correct answer.** Each brief says "place it with
   the other case slides", "place it in the appendix" or "place it in the financing section". The
   correct position satisfies the brief; so does the literal default (append to the block).
2. **A placement rule inside the deck**, where a diligent analyst reads: slide body text on a section
   divider (I1), speaker notes of a section divider (I2), or a footnote text box on the Agenda (I3).
   Never hidden slides or metadata. The rule refines the brief and never contradicts it.
3. **Everything else easy and locally checkable**: numbers copied from `model_outputs.xlsx`,
   duplicate-this-layout, leave-the-reference-slide-unchanged, exact title given in the brief.
4. **A deterministic grader** (`grade.py`) whose checks are all text/structure comparisons, so the only
   realistic way to fail is placement or structure.

## Materials

| Path | What it is |
| --- | --- |
| `generate.py` | Builds the frozen workbook, the base decks (one rule location each), the briefs, the control briefs and `expected/` for all seven instances. Deterministic; `--instances a,b` rebuilds a subset. |
| `grade.py` | `python3 grade.py <output.pptx> <instance_dir>` prints JSON with per-check pass/fail and `strict_pass`. Exit code 0 only on strict pass. |
| `run.py` | Runs the Claude Code CLI as the agent under test in a fresh workdir per run, grades the result, records the models used and summarises the transcript. |
| `instances/<id>/brief.md` | The artefact-rule brief (the rule is only in the deck). |
| `instances/<id>/brief_control.md` | Same brief plus one sentence stating the deck's rule verbatim (paired control). |
| `instances/<id>/brief_anchor.md` | v1 instances only: same brief with the placement sentence replaced by a stronger, still true, literal anchor (supplementary variant; see the v1 pilot results). In the v2 instances I4, I5 and I6 the anchor is part of `brief.md` itself. |
| `instances/<id>/inputs/` | `ic_deck_base.pptx` (16 slides; 30 for I6) and `model_outputs.xlsx` (frozen, fictional; extended to eight cases and nine schedule tabs for I6 only). This is all the agent sees. |
| `instances/<id>/expected/` | `spec.json` (expected title order, values, template slide, rule text) and `expected_order.txt`. Never copied into an agent workdir. |
| `tests/` | `make_fixtures.py` builds a hand-made correct output and a deliberately misplaced output per instance (plus a workbook-tab-order decoy for I2b); `test_grader.py` asserts the grader passes the former and fails the others on `title_order` only. |

### The base deck (16 slides; I6 uses a 30-slide expansion described under v2 instances)

1. Title. 2. Agenda (lists sections and the case list; carries a small footnote text box).
3. Executive summary. 4. Section divider "Cases". 5–7. Case 1, 2, 3 cards built from the custom slide
layout **Case card** (title, four metric tiles, a 4x2 table, a source note). 8. Section divider
"Financing and covenant". 9. Covenant: monthly DSCR and sponsor support. 10. Funding: sources and uses.
11. Recommendation. 12. Closing. 13. Section divider "Appendix". 14. Appendix: DSCR summary and
15. Appendix: Sponsor return (custom layout **Schedule**: title, 5x4 table, source note).
16. **Layout reference: Case card**: `[Fill]` placeholders and the note "Reference slide. Duplicate this
layout for new case slides. Do not edit this slide."

Every slide has speaker notes so that notes are a normal place to look, not a tell.

### The frozen workbook

Tabs in order: Read me, Case summary, DSCR summary, Support cap, Sponsor return, Sensitivity.
Four Northstar Compute cases (Base; Delayed usage receipt; Major operating incident; Renewal without
credit transfer) with minimum operating and post-cure monthly DSCR, sponsor support used against the
cap, sponsor IRR, total receipts, total debt service and closing cash. All figures are fictional and
labelled as such; the tabs are mutually consistent.

## Instances

| Id | New slide | Rule location | Rule text | Brief placement wording | Correct position | Literal default |
| --- | --- | --- | --- | --- | --- | --- |
| `i1_case4` | `Case 4 — Renewal without credit transfer` (Case card) | Body of the "Cases" divider | Case slides are grouped by scenario family rather than by case number: a renewal variant is presented immediately after its base case, before the delayed-receipt and operating-incident cases. | "place it with the other case slides", "update the agenda" | After Case 1, before Case 2 (agenda mirrors: 1, 4, 2, 3) | After Case 3 |
| `i2_schedule` | `Appendix: Support-cap utilisation` (Schedule) | Speaker notes of the "Appendix" divider | Supporting schedules appear in the order of the workbook tabs they are drawn from; a new schedule is inserted at that position, never appended at the end. | "place it in the appendix" | Between DSCR summary and Sponsor return (tab order) | After Sponsor return |
| `i3_sensitivity` | `Sensitivity: DSCR with support cap minus 20%` (Case card) | Footnote text box on the Agenda | Deck conventions: Recommendation always immediately precedes Closing; a sensitivity slide is placed directly after the slide it sensitises. | "place it in the financing section" | Directly after "Covenant: monthly DSCR and sponsor support" | After "Funding: sources and uses" |
| `i2b_schedule_first` (v2) | `Appendix: Support-cap utilisation` (Schedule) | Speaker notes of the "Appendix" divider | Appendix convention: a newly added schedule is inserted directly after this Appendix divider, ahead of the existing schedules, so that the committee sees new material first. Schedules are never appended at the end of the appendix and are not ordered by workbook tab. | "place it in the appendix" | Directly after the "Appendix" divider, before DSCR summary | After Sponsor return; **decoy**: between DSCR summary and Sponsor return (workbook tab order, the v1 I2 answer) |
| `i4_sensitivity_anchor` (v2) | `Sensitivity: DSCR with support cap minus 20%` (Case card) | Footnote text box on the Agenda | Deck conventions: a sensitivity slide is placed directly after the slide it sensitises; Recommendation always immediately precedes Closing. | strong anchor (below) | Directly after "Covenant: monthly DSCR and sponsor support" | After "Funding: sources and uses" |
| `i5_sensitivity_notes_anchor` (v2) | same as I4 | Speaker notes of the "Financing and covenant" divider | Section convention: a sensitivity slide is placed directly after the slide it sensitises, never at the end of the section. | strong anchor (below) | Directly after "Covenant: monthly DSCR and sponsor support" | After "Funding: sources and uses" |
| `i6_sensitivity_scale` (v2) | same as I4 | Footnote text box on the Agenda (stated once) | same as I4 | strong anchor (below) | Directly after "Covenant: monthly DSCR and sponsor support" (slide 18 of 31) | After "Funding: sources and uses" |

Each rule admits exactly one position. The full expected title order is in
`instances/<id>/expected/expected_order.txt`.

### v2 instances

The v1 pilot (`research/baselines/artifact-rule-pilot/`) found that only I2 (rule in speaker notes) failed, and
only on Sonnet 5.5; Opus 5.5 passed it, but two of its passes never read the notes and inferred the position
from workbook tab order, which happened to be the right answer. The v2 instances remove that coincidence and
add the brief ingredient that reproduced the original DocOps failure: a strong, true, literal anchor.

**The v2 anchor** (I4, I5, I6), used verbatim as step 4 of the brief:

> Place it in the financing section, ahead of the Recommendation slide (that is, anywhere between the
> "Financing and covenant" divider and the Recommendation slide).

Covenant, Funding and Recommendation are consecutive, so "after Covenant" and "after Funding" both satisfy the
anchor literally; only the deck's rule decides between them. The parenthetical rules out the reading
"immediately before Recommendation" that made the v1 I3 anchor ambiguous: a position directly after Covenant is
explicitly inside the stated range, so the brief never contradicts the rule. The paired control (anchor plus
the rule quoted in the brief) passed 3/3 on Sonnet 5.5 before any artefact run was made, so the wording is
followable.

**Would a diligent human analyst find and apply each rule, and why does the brief not contradict it?**

- **I2b.** A deck's speaker notes are where presenters keep conventions, and the analyst is editing the
  appendix, so reading the Appendix divider (body and notes) before inserting a slide there is ordinary
  diligence; the notes are one sentence long and name the exact position. The brief says only "place it in
  the appendix", which the correct position satisfies. The workbook's Read me tab lists the tabs in order and
  labels three of them "appendix schedule"; that describes the workbook, not the deck, and the rule says
  explicitly that schedules are not ordered by workbook tab, so an analyst who read both would not be torn.
- **I4.** The Agenda is the second slide of a 16-slide deck and its footnote is visible body text that any
  text dump shows; the footnote is headed "Deck conventions". The slide being added sensitises the covenant
  DSCR, and the Covenant slide is the only slide about the covenant DSCR, so "directly after the slide it
  sensitises" has one reading. The anchor allows any position between the divider and Recommendation; after
  Covenant is in that range. The brief therefore under-determines placement and the rule refines it.
- **I5.** Same reasoning as I4 for the brief. The rule lives in the speaker notes of the divider that opens
  the very section the analyst is inserting into; an analyst who opens the section divider to see how the
  section is organised would read them. Every slide in the deck has notes, so notes are not a tell.
- **I6.** Same as I4; the deck is 30 slides and the rule is stated once, on the Agenda footnote, with no
  reminder on the Financing divider. A diligent analyst still reads the Agenda of a deck before restructuring
  it. The extra slides (three front-matter slides, eight case cards, eight schedules) do not mention
  placement at all, so nothing competes with the rule; the question is only whether it gets lost at scale.

For I2b the grader additionally reports `matches_decoy_placement` (the workbook-tab-order position) in the
`title_order` detail, so a pass cannot be mistaken for a tab-order inference and a failure can be classified
as "appended" or "tab order".

## Grader checks

All checks are computed from the output deck, the input deck and `expected/spec.json`:

- `slide_count`, `new_slide_present`: exactly one new slide with the exact title (dashes and whitespace normalised).
- `title_order`: the full slide-title sequence equals the expected order. The detail also reports whether the output matches the literal default placement.
- `existing_slides_order_preserved` (diagnostic): the pre-existing slides keep their relative order.
- `new_slide_structure`: same slide-layout name, same shape count and the same multiset of (shape type, placeholder type, table dimensions) as the template slide (the reference slide for case cards, "Appendix: DSCR summary" for the schedule).
- `new_slide_values`: every tile and table row carries the workbook value (number extraction, tolerant of k/m and %-scaling; string values such as "n/a" by substring).
- `new_slide_no_placeholders_left`: no `[Fill]` or reference-slide boilerplate remains.
- `reference_unchanged`: the reference slide's layout, shape count, per-shape text, picture count and notes are identical to the input.
- `agenda_updated` (I1 only): the agenda mentions Case 4, lists the cases in deck order and keeps every original line.
- `other_slides_unchanged`: every other input slide (matched by title) has identical shape texts, shape count, notes and layout.

`strict_pass` is the conjunction of all checks. `placement_pass` and `all_non_placement_pass` are reported
separately so that placement failures can be isolated.

## How to run

```bash
python3 generate.py                     # rebuild instances/ (deterministic)
python3 tests/make_fixtures.py          # hand-made correct and misplaced outputs
python3 tests/test_grader.py            # grader self-test; must print ALL TESTS PASSED

# grade a single output
python3 grade.py path/to/output.pptx instances/i1_case4

# pilot matrix (needs the claude CLI): fresh workdir per run, 15-minute cap, stream-json transcript
python3 run.py --out /path/to/runs --runs 5                                   # default model, both conditions
python3 run.py --out /path/to/runs --runs 3 --conditions artefact --model claude-opus-5-5
python3 run.py --out /path/to/runs --runs 5 --conditions anchor --instances i1_case4,i3_sensitivity
# v2 matrix (see research/baselines/artifact-rule-pilot-v2/)
python3 run.py --out /path/to/runs --runs 5 --conditions artefact --model claude-opus-5-5 \
    --instances i5_sensitivity_notes_anchor,i4_sensitivity_anchor,i2b_schedule_first,i6_sensitivity_scale
```

`run.py` invokes `claude -p "<brief> ... edit inputs/ic_deck_base.pptx in place, keep the filename, do not
read anything outside this directory" --permission-mode acceptEdits --allowedTools Bash,Read,Write,Edit,Glob,Grep
--output-format stream-json --verbose`, records the model names from the result's `modelUsage`, grades the
deck, and writes `run.json` per run with: grade, models used, tool-call counts, whether the rule text ever
appeared in a tool result, whether the agent quoted it, whether it rendered thumbnails (`rendered_thumbnails`), whether any tool input mentioned notes parts
(`read_notes`, a weak signal: listing `ppt/notesSlides` counts), and the agent's final message. The agent's workdir never contains `expected/` or `grade.py`.

## Anchor variant (supplementary, v1 instances)

`brief_anchor.md` keeps everything in `brief.md` but replaces the placement sentence with a stronger literal
anchor that is still true under the correct answer: "before the 'Financing and covenant' divider" (I1),
"before the 'Layout reference: Case card' slide" (I2), "before the Recommendation slide" (I3). It mimics the
wording of the task that motivated this benchmark. Run it with `--conditions anchor`. Note that the I3 anchor
can be read as "immediately before", which the v1 pilot write-up flagged as a confound; the v2 instances I4, I5
and I6 use the unambiguous anchor described above instead.

## Paired control

`brief_control.md` is `brief.md` plus one sentence stating the deck's rule verbatim and where it lives (for the
v2 instances the rule is quoted and followed by "Apply it when placing the new slide.").
Same inputs, same grader. If the control condition fails for an instance, the instance is badly specified
(the agent cannot do the edit even when told the rule) and its artefact-condition result must not be read
as a convention-integration failure.
