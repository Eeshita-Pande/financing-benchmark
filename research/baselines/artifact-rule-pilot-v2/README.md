# Artifact-rule pilot v2: results

Second pilot of `tasks/artifact-rule/` (PowerPoint-only placement task) against the Claude Code CLI as the agent
under test, on the four v2 instances (`i2b_schedule_first`, `i4_sensitivity_anchor`,
`i5_sensitivity_notes_anchor`, `i6_sensitivity_scale`). Run on 13 October 2026 from a cloud container with
`run.py`: fresh working directory per run containing only `brief.md` and `inputs/`, 15-minute cap,
`--permission-mode acceptEdits`, `--allowedTools Bash,Read,Write,Edit,Glob,Grep`, `stream-json` transcript,
graded with `grade.py`. Models are the `modelUsage` keys of each run's result event (every run also lists
`claude-haiku-5-5`, which the CLI uses for side tasks; it is not the agent model). "Sonnet" below is the CLI's
default model, which `modelUsage` reported as `claude-sonnet-5-5` in every default run; "Opus" is
`--model claude-opus-5-5`.

Raw per-run records are in `results.json` (produced by `analyze.py` from the `run.json` files); each group
lists every run with its position label, whether the rule text appeared in any tool result, whether the agent
quoted it, whether it read notes or rendered thumbnails, and the agent's final message.

## What changed from v1

| Instance | Rule location | Rule | Brief placement sentence | Correct | Literal default | Decoy |
| --- | --- | --- | --- | --- | --- | --- |
| I2b | Appendix divider speaker notes | New schedules go directly after the divider, ahead of the existing schedules; never appended; not workbook-tab order | "Place it in the appendix." | After divider (slide 14) | After Sponsor return (slide 16) | Workbook tab order, between DSCR summary and Sponsor return (slide 15) |
| I4 | Agenda footnote | Sensitivity slide directly after the slide it sensitises; Recommendation immediately precedes Closing | Strong anchor: "ahead of the Recommendation slide (that is, anywhere between the 'Financing and covenant' divider and the Recommendation slide)" | After Covenant (slide 10) | After Funding (slide 11) | none |
| I5 | Financing divider speaker notes | Sensitivity slide directly after the slide it sensitises, never at the end of the section | Same anchor | After Covenant (slide 10) | After Funding (slide 11) | none |
| I6 | Agenda footnote, stated once, 30-slide deck | Same as I4 | Same anchor | After Covenant (slide 18) | After Funding (slide 19) | none |

The paired control brief for each instance is the artefact brief plus the rule quoted verbatim with its location
and "Apply it when placing the new slide."

## Run matrix

Specified matrix: artefact condition x 5 runs per instance on Opus and on Sonnet; control condition x 3 runs
per instance on Sonnet; 3 Opus control runs for each instance where Opus failed the artefact condition (I2b
and I6). Everything specified ran; nothing was skipped. Totals: 58 runs (20 Opus artefact, 20 Sonnet artefact, 12 Sonnet control, 6 Opus control; the 3 Sonnet I4 control runs were
made first, before any artefact run, to validate the anchor wording), 0 timeouts, 0 agent errors, 45 minutes of agent wall
time, about USD 13.3 of API cost as reported by the CLI.

| Instance | Condition | Model | n | Strict pass | Placement pass | Non-placement checks all pass | Literal default | Decoy (tab order) | Rule text seen in a tool result | Rendered thumbnails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I2b (notes rule, vague brief, decoy) | artefact | Opus | 5 | **2/5** | 2/5 | 5/5 | 0 | 3 | 2 | 0 |
| I2b | artefact | Sonnet | 5 | **0/5** | 0/5 | 5/5 | 5 | 0 | 0 | 0 |
| I2b | control | Sonnet | 3 | 3/3 | 3/3 | 3/3 | 0 | 0 | 3 | 0 |
| I2b | control | Opus | 3 | 3/3 | 3/3 | 3/3 | 0 | 0 | 3 | 0 |
| I4 (agenda rule, strong anchor) | artefact | Opus | 5 | 5/5 | 5/5 | 5/5 | 0 | – | 5 | 0 |
| I4 | artefact | Sonnet | 5 | 5/5 | 5/5 | 5/5 | 0 | – | 5 | 3 |
| I4 | control | Sonnet | 3 | 3/3 | 3/3 | 3/3 | 0 | – | 3 | 0 |
| I5 (notes rule, strong anchor) | artefact | Opus | 5 | 5/5 | 5/5 | 5/5 | 0 | – | 5 | 0 |
| I5 | artefact | Sonnet | 5 | **2/5** | 2/5 | 5/5 | 3 | – | 2 | 0 |
| I5 | control | Sonnet | 3 | 3/3 | 3/3 | 3/3 | 0 | – | 3 | 0 |
| I6 (agenda rule, strong anchor, 30 slides) | artefact | Opus | 5 | **4/5** | 4/5 | 5/5 | 1 | – | 5 | 0 |
| I6 | artefact | Sonnet | 5 | 5/5 | 5/5 | 5/5 | 0 | – | 5 | 0 |
| I6 | control | Sonnet | 3 | 3/3 | 3/3 | 3/3 | 0 | – | 3 | 0 |
| I6 | control | Opus | 3 | 3/3 | 3/3 | 3/3 | 0 | – | 3 | 0 |

Per-check pass rates: in every group, every run passed `file_opens`, `slide_count`, `new_slide_present`,
`existing_slides_order_preserved`, `new_slide_structure`, `new_slide_values`, `new_slide_no_placeholders_left`,
`reference_unchanged` and `other_slides_unchanged`. The only check that ever failed, in any of the runs, was
`title_order` (the per-check counts are in `results.json` under `per_check_pass`). As in v1, the grader never
produced a non-placement failure, so "only realistic way to fail is placement" still holds, now across 30-slide
decks and schedule slides as well.

Every pass in every group had the rule text in at least one tool result ("Rule text seen" equals the pass
count in all artefact groups except I6 Opus, where the one failing run also saw it). There were therefore no
coincidental passes of the kind the v1 pilot found on I2: the I2b decoy did its job.

Other observations: no run timed out and no run returned an agent error. Opus runs were slower (mean 33 to
128 s per group, with 6 runs between 170 and 191 s because of a stalled heredoc the agent had to recover
from) and roughly three times the cost of Sonnet runs. Three Sonnet runs on I4 rendered the deck with
LibreOffice and inspected a PNG of the new slide; all three passed, so thumbnail checks were neither
necessary nor harmful here. Four Sonnet runs left stray files in the working directory (a helper script, an
unzip directory, a backup copy); several Opus runs wrote scratch files to paths outside the working directory
despite the instruction not to. Neither affects grading.

## Failed runs

Every failed run is listed here with the four signals the analysis asked for: did the rule text appear in any
tool result, did the agent mention it, did it render thumbnails, and where did it put the slide.

### I2b, artefact, Opus: 2/5 (confirmed repeat on a frontier model)

All three failures placed the schedule in the **decoy** position (slide 15, between "Appendix: DSCR summary"
and "Appendix: Sponsor return"), that is, workbook tab order. In none of the three did the rule text ever
appear in a tool result; none mentioned it; none rendered thumbnails.

- r1 (4 tool calls, 31 s): dumped every slide's shapes and text with python-pptx (no notes), unzipped the
  deck to read `slide14.xml` and its rels, then read the speaker notes **of slides 14, 15 and 16 only** (the
  two schedules and the reference slide), never slide 13 (the divider). Final message: "The new slide is
  slide 15, between 'DSCR summary' (14) and 'Sponsor return' (16). That matches the tab order in the
  workbook."
- r3 (4 tool calls, 32 s): same sequence; read the notes XML of slides 14 to 16 from the unzipped package;
  never the divider's. Final message: "I added the support-cap schedule as a new slide 15".
- r5 (4 tool calls, 34 s): dumped slide text, printed the agenda body and the XML tree of slide 14, copied
  the DSCR summary slide, inserted it after it. Final message: "It sits between 'Appendix: DSCR summary' and
  'Appendix: Sponsor return', which follows the tab order in the workbook."

The two passes (r2, r4) read the notes of every slide in their first or second tool call, saw the convention
and inserted the slide directly after the divider; neither quoted the rule verbatim but both described it.

### I2b, artefact, Sonnet: 0/5 (confirmed repeat)

All five appended the schedule at the end of the appendix (slide 16, after "Appendix: Sponsor return"), the
**literal default**. None had the rule text in a tool result, none mentioned any convention, none rendered
thumbnails. Three of the five (r1, r4, r5) read speaker notes, but only those of the schedule slide(s) they were
copying (Sponsor return, and in r4 also DSCR summary), never the divider's; r2 and r3 read no notes at all (two
tool calls each). All five described the position as "after 'Appendix: Sponsor return'" or "the last schedule
in the appendix" without further justification. Sonnet never chose the decoy position: its default is to
append, not to reason about tab order.

### I5, artefact, Sonnet: 2/5

All three failures placed the slide after "Funding: sources and uses" (slide 11), the **literal default**,
immediately before Recommendation. None had the rule text in a tool result, none mentioned a convention, none
rendered thumbnails. All three read speaker notes, but only those of the slides they were copying or checking
(a case card and the reference slide; r1 also a schedule), never the Financing divider's. r3 also had the agenda
footnote (neutral in I5) in a tool result.

- r1 (6 calls): "The slide is slide 11, after 'Funding: sources and uses' and before 'Recommendation'."
- r3 (5 calls): "It's slide 11, between 'Funding: sources and uses' and 'Recommendation', in the financing
  section."
- r4 (6 calls): "it is slide 11, after 'Funding: sources and uses'".

The two passes (r2, r5, three tool calls each) dumped slide text **and notes** for every slide in their first
call, saw the section convention and placed the slide after Covenant.

### I6, artefact, Opus: 4/5

- r3 (12 tool calls, 191 s): placed the slide after Funding (slide 19), the **literal default**. The rule text
  **was** in a tool result (the agent's first python-pptx dump printed the agenda footnote), the agent read it,
  and its final message named it and explained why it overrode it: "a footnote on the Agenda slide says a
  sensitivity slide goes directly after the slide it sensitises. The workbook says this sensitivity is on a
  'Case 2 basis', so that rule would put it after Case 2 in the Cases section. I followed your brief and put it
  in the financing section instead." No thumbnails. This is the DocOps pattern (rule read, named, overridden
  in favour of the brief's literal wording), but it rests on a competing reading of "the slide it sensitises":
  the agent took the sensitivity's *basis case* (Case 2) as the sensitised slide rather than the covenant
  analysis the brief says it sensitises. See the caveat below.

The other four Opus runs and all five Sonnet runs read the footnote and placed the slide after Covenant.

## Control condition and specification

No instance failed its control: Sonnet 3/3 on all four instances, Opus 3/3 on I2b and I6 (the two instances
where Opus failed the artefact condition). Every instance is therefore doable when the rule is stated in the
brief, and the artefact-condition failures are convention-integration failures, not editing failures.

One specification caveat should be fixed before the task is used as a benchmark. **The I4/I5/I6 rule admits a
second reading.** The workbook's Sensitivity tab labels the row "DSCR with support cap minus 20% (Case 2
basis)", so "the slide it sensitises" can be read as the Case 2 card rather than the Covenant slide. The brief
and the anchor both put the slide in the financing section, so an agent that takes the Case 2 reading sees a
conflict and, reasonably, follows the brief. In this pilot that reading occurred once in 30 artefact runs
(I6 Opus r3) and zero times in the 9 Sonnet control runs; everywhere else the agent resolved "the slide it
sensitises" to the Covenant slide. Fix for a v3: either drop "(Case 2 basis)" from the workbook row label
(move it to the Read me tab) or phrase the rule as "a sensitivity slide is placed directly after the analysis
slide it sensitises (for the covenant DSCR, the Covenant slide)". The I2b rule has no such ambiguity: it names
the position ("directly after this Appendix divider, ahead of the existing schedules").

## Reading of the result

**Which instance a frontier model fails on repeat:** `i2b_schedule_first`. Opus 5.5 failed 3 of 5 artefact
runs and passed 3/3 controls; Sonnet 5.5 failed 5/5 and passed 3/3 controls. I6 produced one Opus failure in
five, of the rule-overridden kind, but it is confounded by the rule ambiguity above and is not yet a confirmed
repeat.

**Minimal ingredients that produce the failure, from the four instances together:**

1. **The rule is in speaker notes, not in visible slide text.** Every visible-text rule (I4 and I6 agenda
   footnote) was found by both models in 20 of 20 runs, because any slide-text dump prints it. Notes are only
   seen if the agent chooses to print them.
2. **The notes belong to a slide the agent has no editing reason to open.** Across all 11 failed runs on I2b
   and I5, the agent read the speaker notes of the slide it was duplicating (and sometimes the reference
   slide), and never the divider's. Every one of the passes on those two instances came from a run that dumped
   the notes of *all* slides in one go. Opus does that more often than Sonnet (10/10 on I4/I5, 2/5 on I2b), which
   is why I5 did not fail Opus and I2b did: the appendix workflow (copy a schedule, read its notes and XML)
   gives Opus a complete-looking picture without the divider.
3. **A plausible alternative inference that the brief does not rule out.** In I2b the workbook's Read me
   lists the tabs in order and the existing schedules follow that order, so "insert in tab order" looks like
   the deck's convention; the rule says the opposite. Removing the coincidence between the natural inference
   and the correct answer is what turned v1's I2 (Opus 5/5) into I2b (Opus 2/5). Sonnet does not make the
   inference and simply appends.
4. **A vague placement sentence.** "Place it in the appendix" is true under the correct answer, the decoy
   and the literal default. The strong anchor used in I4 to I6 did *not* add failures for visible rules once it
   was made unambiguous (I4 Sonnet 5/5 versus v1 I3-anchor 3/5), so the anchor is not an ingredient of the
   I2b failure; it is an ingredient of the rule-overridden pattern seen once in I6 and in v1's I3 anchor runs.

Ingredients that did **not** matter: deck scale (I6 Sonnet 5/5, Opus 4/5 with the one failure unrelated to
scale); thumbnail rendering (never used by a failing run; three passing Sonnet runs rendered). Everything
else in the task (duplication, values, locked reference slide, untouched slides) was done correctly in all
runs, so the benchmark isolates the placement decision as intended.

## Reproduce

```bash
cd tasks/artifact-rule
python3 tests/test_grader.py                     # grader self-test (all seven instances)
V2=i5_sensitivity_notes_anchor,i4_sensitivity_anchor,i2b_schedule_first,i6_sensitivity_scale
python3 run.py --out /tmp/runs --runs 5 --conditions artefact --instances $V2 --model claude-opus-5-5
python3 run.py --out /tmp/runs --runs 5 --conditions artefact --instances $V2          # Sonnet default
python3 run.py --out /tmp/runs --runs 3 --conditions control  --instances $V2
python3 run.py --out /tmp/runs --runs 3 --conditions control  --instances i2b_schedule_first,i6_sensitivity_scale --model claude-opus-5-5
python3 ../../research/baselines/artifact-rule-pilot-v2/analyze.py /tmp/runs results.json
```

`run.py` removes `CLAUDE_CODE_SESSION_ID` and related variables from the child environment, as in v1. The
nested CLI's transcripts still carried the orchestrating session's id in their `session_id` field, so the
variable is not the only channel; it had no visible effect on the runs.
