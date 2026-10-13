# PowerPoint benchmarks: what we learned, what we built, how to run it

Date: 2026-10-13. Companion to `slide-benchmark-review.md` (the survey) and the baseline and task
branches listed at the end.

## Learnings from the benchmark review

Slide benchmarks are about eighteen months old and none is an industry standard yet, but three are
credible enough to quote: PPT-Eval (Microsoft and CMU, ICML 2026), PPTArena (ECCV 2026, the editing
baseline every newer paper compares against) and BankerToolBench (Handshake AI with 502 bankers, the only
one that grades finance decks professionally). Across them, and DocOps for office-file workflows, the same
picture holds: models can already read a deck, make single edits and produce a deck that opens, and those
abilities are saturated. What still fails is verification discipline rather than capability. Agents change
content without re-checking layout, drop sub-edits in compound instructions, do not reuse the deck's own
conventions, and lose track of state across files. Two warnings from running the benchmarks ourselves:
several hard cases in PPTArena measure agreement with one annotator rather than skill, because the
instruction is ambiguous and the reference deck is itself flawed, and DocOps ships verifier expectations
and mismatched output names into the agent's working directory, so its headline numbers are not a clean
capability measure. The design rule we took from this is that a task must be unambiguous, graded
deterministically on the native file, and paired with a control that isolates the capability being tested.

## What we did, and what failed

- Surveyed about twenty benchmarks and picked five to run. See `slide-benchmark-review.md`.
- PPTArena: identified 46 failing cases from the repo's recorded scores, ran 11 of them with Claude Code.
  All produced valid decks; failures were layout reflow after an edit, ambiguous instructions resolved
  differently from the reference, and new charts not matching deck style. Official judges were unreachable,
  so scores are Claude-judged and directional only. Branch `claude/baseline-pptarena`.
- PPT-Eval: inventoried all 120 tasks and the 30-task hard tier, built a working harness, but ran nothing,
  because the source decks are on archive.org, which the environment's network policy blocks.
  Branch `claude/baseline-ppteval`.
- DocOps: ran 12 PowerPoint and cross-document tasks in both skill modes with the benchmark's own verifiers,
  plus Opus re-runs of every failure. Strict pass rates were L1 2/2, L3 1/3, L4 1/7, but most L4 failures
  are benchmark packaging defects. The one genuine, repeatable failure is a slide-placement rule stated
  inside the deck that every agent ignored five times out of five. Branch `claude/baseline-docops`.
- BankerToolBench: not run. Its data is on huggingface.co (blocked) and it needs the Docker daemon.
- Built our own task from the DocOps failure ("artifact-rule"): a frozen workbook, a 16-slide committee
  deck, a brief that is true but under-determined, a placement rule inside the deck, a deterministic grader,
  and a paired control with the rule copied into the brief. Version 1: rules in visible slide text were
  always found; only the rule in speaker notes failed Sonnet (0/5), and Opus passed it by coincidence with
  workbook tab order. Version 2 removed the coincidence. Instance I2b now fails Opus 5.5 three times out of
  five and Sonnet 5.5 five out of five, with both passing the control three out of three. Every one of 109
  runs across both versions passed every non-placement check; slide order is the only thing that ever fails.
  Branches `claude/task-artifact-rule` and `claude/task-artifact-rule-v2`.
- Minimal ingredients for the failure: the rule is in speaker notes, on a slide the agent has no editing
  reason to open, the brief does not exclude a plausible wrong inference, and the placement sentence is vague.
- Process failures worth knowing: the usage limit stopped one child mid-run and a container was recycled;
  the Claude Code CLI defaults to Sonnet 5.5, so the agent model must be recorded per run; the permission
  classifier refused the skip-permissions flag, so runs use an allow-list instead.

## Run it in a few minutes

Prerequisites: Python 3.12+, `pip install python-pptx openpyxl`, and the `claude` CLI installed and logged
in. Each agent run takes 20 to 40 seconds.

```bash
git fetch origin claude/task-artifact-rule-v2
git checkout claude/task-artifact-rule-v2
cd tasks/artifact-rule
python3 tests/test_grader.py            # grader self-test, prints ALL TESTS PASSED

# the failing instance, 2 runs each with the rule in the deck and with the rule in the brief (about 3 minutes)
python3 run.py --out /tmp/runs --runs 2 --instances i2b_schedule_first --conditions artefact,control
python3 run.py --out /tmp/runs --runs 2 --instances i2b_schedule_first --conditions artefact --model claude-opus-5-5
```

Where to look afterwards:

- `/tmp/runs/<instance>__<condition>__<model>__r<N>/run.json`: grade per check, the position the agent chose,
  the model used, tool calls, whether the rule text ever appeared in a tool result, and the agent's final
  message. `title_order: false` with everything else true is the failure.
- The same folder holds the agent's working directory with the edited deck (`inputs/ic_deck_base.pptx`)
  and the full `stream-json` transcript, so you can open the deck and read what the agent did.
- `python3 grade.py <that deck> instances/i2b_schedule_first` re-grades any output by hand.
- The rule the agent missed is in the speaker notes of the "Appendix" divider slide; the brief it was
  given is `instances/i2b_schedule_first/brief.md`, and the control brief is `brief_control.md`.
- Pilot results and per-run narratives: `research/baselines/artifact-rule-pilot-v2/README.md` and
  `results.json` (grouped by instance, condition and model).

## Branches and pull requests

- `claude/ecstatic-lamport-7hw0h7`: survey and this summary (PR #1).
- `claude/baseline-ppteval` (PR #2), `claude/baseline-pptarena` (PR #3), `claude/baseline-docops` (PR #4).
- `claude/task-artifact-rule` (PR #5), `claude/task-artifact-rule-v2` (PR #6, contains everything in v1).
