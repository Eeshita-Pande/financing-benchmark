# Artifact-rule pilot: results

Pilot of `tasks/artifact-rule/` (PowerPoint-only placement task) against the Claude Code CLI as the agent
under test. Run on 13 October 2026 from a cloud container with `run.py`; every run used a fresh working
directory containing only `brief.md` and `inputs/`, a 15-minute cap, `--permission-mode acceptEdits`,
`--allowedTools Bash,Read,Write,Edit,Glob,Grep`, and the `stream-json` transcript was graded with `grade.py`.
Models are taken from the `modelUsage` keys of each run's result event (every run also lists
`claude-haiku-5-5`, which the CLI uses for side tasks; it is not the agent model).

Raw per-run records (grade, tool calls, whether the rule text ever appeared in a tool result, whether the
agent quoted it, whether thumbnails were rendered, final message) are in `results.json`, produced by
`analyze.py` from the 51 `run.json` files.

## Run matrix

| Instance | Condition | Model | n | Strict pass | Placement pass | Non-placement checks all pass | Rule text seen in a tool result | Rendered thumbnails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| i1_case4 (rule in divider body) | artefact | claude-sonnet-5-5 | 5 | **5/5** | 5/5 | 5/5 | 5 | 0 |
| i1_case4 | control | claude-sonnet-5-5 | 5 | 5/5 | 5/5 | 5/5 | 5 | 0 |
| i1_case4 | artefact | claude-opus-5-5 | 3 | 3/3 | 3/3 | 3/3 | 3 | 1 |
| i2_schedule (rule in speaker notes) | artefact | claude-sonnet-5-5 | 5 | **0/5** | 0/5 | 5/5 | 0 | 0 |
| i2_schedule | control | claude-sonnet-5-5 | 5 | 5/5 | 5/5 | 5/5 | 5 | 0 |
| i2_schedule | artefact | claude-opus-5-5 | 3 (+2 supplementary = 5) | 5/5 | 5/5 | 5/5 | 3 | 0 |
| i3_sensitivity (rule in agenda footnote) | artefact | claude-sonnet-5-5 | 5 | **5/5** | 5/5 | 5/5 | 5 | 0 |
| i3_sensitivity | control | claude-sonnet-5-5 | 5 | 5/5 | 5/5 | 5/5 | 5 | 0 |
| i3_sensitivity | artefact | claude-opus-5-5 | 3 | 3/3 | 3/3 | 3/3 | 3 | 0 |

Supplementary (added after the specified matrix, same inputs and grader):

| Instance | Condition | Model | n | Strict pass | Placement pass | Non-placement all pass | Rule seen |
| --- | --- | --- | --- | --- | --- | --- | --- |
| i1_case4 | anchor | claude-sonnet-5-5 | 5 | 5/5 | 5/5 | 5/5 | 5 |
| i3_sensitivity | anchor | claude-sonnet-5-5 | 5 | **3/5** | 3/5 | 5/5 | 5 |

"anchor" is `brief_anchor.md`: the artefact brief with the placement sentence replaced by a stronger but
still true literal anchor ("Place it with the other case slides, before the 'Financing and covenant'
divider" / "Place it in the financing section, before the Recommendation slide"). It mimics the
"place it before Closing" wording of the DocOps task that motivated this benchmark.

Totals: 51 runs (39 specified + 2 supplementary Opus + 10 anchor), 0 timeouts, 0 agent errors,
30 minutes of wall time, about USD 9.9 of API cost. Slowest run 150 s; most runs 20 to 40 s.
Every run passed every non-placement check (structure, values, reference slide, other slides, no
leftover placeholders, agenda where required). The only check that ever failed was `title_order`.

## Confirmed repeats and what the failed runs did

**i2_schedule, artefact, Sonnet 5.5: 0/5, a confirmed repeat.** All five runs appended the new schedule
after "Appendix: Sponsor return" (the literal default position). In none of the five did the rule text
ever appear in a tool result.

- r1: Listed the deck as XML, saw the `ppt/notesSlides` directory and `slide14.xml.rels` but never opened
  a notes part; copied the Sponsor return slide and appended it. Final message: "It comes after 'Appendix:
  Sponsor return' and before the 'Layout reference: Case card' slide."
- r2: Read the workbook including the Read me tab's "Tabs, in order" list, grepped slide text for titles
  only, never read any notes. Placed it as slide 16 "directly after 'Appendix: Sponsor return'".
- r3: Same pattern with seven tool calls: unzipped the deck, grepped titles, read the Support cap tab,
  listed notesSlides without reading them. Reported "the last schedule in the appendix".
- r4: Dumped slide text with python-pptx (which does not include notes), copied Sponsor return, appended.
  Reported "right after 'Appendix: Sponsor return'".
- r5: Shortest run (two tool calls): dumped titles and the Support cap tab, duplicated and appended.
  Did not look at notes at all.

**i3_sensitivity, anchor, Sonnet 5.5: 3/5.** Both failures placed the slide after "Funding: sources and
uses" (the literal default) although the rule text was in a tool result in both runs.

- r2: Read the agenda footnote and explicitly acknowledged it: "I didn't put it right after the
  'Covenant' slide. That would also follow the agenda's rule that a sensitivity slide sits directly after
  the slide it sensitises, but your brief said to put it before Recommendation." The brief's anchor was
  read as "immediately before Recommendation", overriding the deck's rule.
- r3: Saw the footnote in the slide dump, did not mention it, and placed the slide "between 'Funding:
  sources and uses' and 'Recommendation'".

No run in any condition rendered thumbnails except one Opus run on i1 (which passed). The failure mode
reproduced here is therefore not "thumbnails pass"; it is "the notes were never read" (i2) or "the
brief's literal anchor outranked the rule" (i3 anchor).

## Instances judged badly specified

None by the control criterion: the control condition passed 5/5 on every instance, so each instance is
doable when the rule is stated in the brief, and the artefact-condition failures are convention-
integration failures, not editing failures.

Two design caveats that should be fixed before this is used as a benchmark:

1. **i2_schedule's correct position coincides with the natural inference from the workbook.** The rule
   (insert in workbook tab order) places the new schedule exactly where an agent that simply mirrors the
   workbook's tab list would put it. Two of the five Opus passes never saw the rule and justified the
   position by "the tab order in the workbook". The instance still discriminates (Sonnet appended 5/5),
   but a pass does not prove the notes were read. Fix: make the rule place the slide somewhere the
   workbook does not suggest, for example "new schedules are inserted directly after the Appendix
   divider, ahead of the existing schedules".
2. **The i3 anchor wording is ambiguous.** "Before the Recommendation slide" can be read as "immediately
   before", in which case the brief contradicts the rule and the failure is a brief-ambiguity failure,
   not an under-determination failure. A v2 anchor should be unambiguous yet strong, for example
   "Place it in the financing section (anywhere between the 'Financing and covenant' divider and the
   Recommendation slide)".

## Reading of the result

- With a vague placement sentence and a rule that sits in visible slide text (divider body, agenda
  footnote), Sonnet 5.5 found and applied the rule in 10/10 artefact runs: a plain python-pptx text dump
  of all slides shows the rule, and the agent then reasons about it.
- With the same vague sentence and the rule in speaker notes, Sonnet 5.5 failed 5/5: its deck inspection
  never covered notes, and it defaulted to appending. Opus 5.5 passed 5/5, reading the notes in 3 of 5
  runs and inferring the same position from workbook tab order in the other 2.
- A stronger literal anchor in the brief is what reproduces the original DocOps behaviour on a visible
  rule: Sonnet 5.5 dropped to 3/5 on i3, and one failing run read the rule, named it and overrode it in
  favour of the brief.
- The grader never produced a non-placement failure in 51 runs, so the task satisfies the "only
  realistic way to fail is placement" requirement.

## Reproduce

```bash
cd tasks/artifact-rule
python3 tests/test_grader.py                     # grader self-test
python3 run.py --out /tmp/runs --runs 5          # Sonnet default, artefact + control
python3 run.py --out /tmp/runs --runs 3 --conditions artefact --model claude-opus-5-5
python3 run.py --out /tmp/runs --runs 5 --conditions anchor --instances i1_case4,i3_sensitivity
python3 ../../research/baselines/artifact-rule-pilot/analyze.py /tmp/runs results.json
```
