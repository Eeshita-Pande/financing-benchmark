# DocOps baseline: Claude Code on PowerPoint and Excel-to-PowerPoint tasks

This directory records a first baseline of Claude Code on
[DocOps](https://github.com/icip-cas/DocOps) (Jiang et al., 2026, arXiv:2607.19865),
a 210-task Harbor benchmark of native Office/PDF document operations with
deterministic artifact-level verifiers. The purpose is to find the task shapes
on which a frontier coding agent still fails, with emphasis on PowerPoint and
cross-document (Excel + PowerPoint) workflows, because those are the closest
public analogue to a financing-deck task (workbook to slides with numbers that
must reconcile).

Everything here was produced in one cloud session on 2026-10-13. Runs were
executed **outside Docker** (the daemon was not available), so the task
environments were materialised by hand; see "Caveats".

## Summary

* 12 PowerPoint-centred DocOps tasks (2 L1, 3 L3, 7 L4; 5 of the L4 tasks are workbook-to-deck or deck-plus-workbook), each run once skill-off and once skill-on with Claude Code (`claude-sonnet-5-5`), plus opus reruns (`claude-opus-5-5`) of the 8 strict failures. 24 + 7 completed runs, all under the 15 min cap, every output file opened cleanly. Runs were outside Docker.
* Strict pass rate (the task's own verifier, as the official harness would score it): L1 2/2 / 2/2, L3 1/3 / 1/3, L4 1/7 / 1/7 (skill-off / skill-on).
* Lenient pass rate (same verifier, pointed at the file the agent actually wrote): L4 3/7 / 3/7.
* The gap between strict and lenient is a benchmark defect, not an agent failure: all 40 v2 L4 tasks name their output files differently in the instruction than in the verifier (section 5.1a). Two more of the sampled v2 tasks require sheet names, slide titles, headings and one numeric constant that appear in no input (5.1b), and 33 v2 L3 tasks ship the verifier's expected values into the agent's container (5.1c).
* Opus reruns of the 8 strict failures (skill-off): 1 of 7 completed reruns passed strictly (`pptwf_001`); the eighth (`l4_065`) did not run because the org spend limit was hit. Opus repeated the board-pack slide-order failure exactly and introduced one new content error (`l4_043`, over-redaction inside the internal workbook).
* The genuine, repeatable agent failures are both of one kind: slide-ordering rules stated inside the deck rather than in the brief (`pptwf_001`, `pptxr_001`). Numbers were never wrong, no file was ever corrupted, and skills changed no outcome.

## 1. Benchmark inventory

DocOps commit `ccf7a75` ("Add citation to README"). `scripts/verify_package.py`
reports 210 tasks, 130 from the v1 set and 80 from the v2 set, with the expected
level split:

| level | meaning | tasks | tasks that involve PPTX |
|---|---|---|---|
| L1 | localized atomic operation on one document | 50 | 12 |
| L2 | compositional, same document | 40 | 10 |
| L3 | single-document multi-step workflow | 60 | 15 |
| L4 | cross-document workflow, usually multi-output | 60 | 14 |

Only 14 L4 tasks involve PowerPoint at all, and only 6 of those pair PowerPoint
with Excel (`ppt+xlsx`, `pptx+xlsx`, `xlsx+ppt`); 2 more pair it with Word and 1
with PDF. The rest of L4 is dominated by Word+Excel (14), PDF+Excel (6) and three-format PDF+Word+Excel packets (5), plus 22 single-format L4 tasks.

The full 210-row table (level, format, number of deliverables, one-line
summary) is in [`inventory.md`](inventory.md).

**Published per-task results.** None are available to us. The repository
contains no result files, the project page (docopsbench.github.io) and arXiv
are blocked by this environment's network policy, and HuggingFace is blocked
too. The paper's headline claim, as relayed in the task brief, is near-collapse
on L4. We therefore treated L3 and L4 PowerPoint and Excel+PowerPoint tasks as
the presumed failing set and sampled from it.

## 2. Agent under test and harness

* Agent: Claude Code CLI `2.1.296`, headless (`claude --print`), permission mode
  `bypassPermissions`, default model of the CLI in this environment, which the
  run records show as `claude-sonnet-5-5` (with `claude-haiku-5-5` used by the
  CLI for small internal calls). DocOps' own Claude Code wrapper defaults to
  `claude-sonnet-4-6`; we did not override the model.
* Tools available to the agent: the normal Claude Code built-ins (Bash, file
  tools). `python`/`python3` on the agent's PATH resolve to a venv containing
  the DocOps `requirements.txt` set (python-pptx 1.0.2, openpyxl 3.1.5,
  python-docx, pdfplumber, pypdf, PyMuPDF, pandas) plus `markitdown`, which the
  bundled skills call. LibreOffice `soffice` is installed. Node 22 is
  installed but `pptxgenjs` (referenced by the pptx skill's "create from
  scratch" path) is not.
* **Skill-off** mode: `--disable-slash-commands`, a fresh `CLAUDE_CONFIG_DIR`,
  `--setting-sources project`, `--strict-mcp-config`, and the session's
  synced-skills env var removed. We verified with a probe prompt that the
  nested agent reports no skills in this configuration. (Without these flags
  the nested CLI inherits Anthropic's own `pptx`/`xlsx`/`docx`/`pdf` skills from
  the hosting session, which would contaminate the skill-off condition.)
* **Skill-on** mode: the same, minus `--disable-slash-commands`, with the
  DocOps `skills/` directory (doc, pdf, pptx, xlsx; byte-identical to every
  task's `environment/skills/`) copied to `<workdir>/.claude/skills/` so the
  agent discovers them as project skills. In Docker, DocOps copies the same
  skills to `/root/.claude/skills/`.
* Materialisation: for each task, exactly the files named by `COPY` lines in
  `environment/Dockerfile` are copied into an empty work directory, and every
  `/root/` path in `instruction.md` and in the verifier's `task_metadata.json`
  is rewritten to that directory. The agent is started with the rewritten
  `instruction.md` as its prompt, in the work directory, with a 900 s wall
  clock cap (DocOps' `task.toml` allows 1200 s).
* Grading: the task's own `tests/test_outputs.py` is run with pytest exactly
  as `tests/test.sh` does (`-rA -v`), with `TASK_METADATA_PATH` pointing at
  the rewritten metadata. Reward is 1 only if every test function passes,
  matching `test.sh`. We additionally record per-test-function outcomes and
  the first failing assertion message. Note that the 130 v1 tasks have a
  single `test_semantic_verifier` function with many assertions, so only the
  first failed check is visible for those; the v2 tasks have 4 to 7 test
  functions.
* Runs were strictly sequential (one agent at a time) after an early parallel
  attempt showed the agent writing `cd /home/user/bench/runs/*/work`, a glob
  that would have matched sibling runs.

All harness code is in this directory under [`tools/`](tools/).

## 3. Chosen tasks and why

12 tasks, each run in skill-off and skill-on mode (24 runs), plus opus
reruns of the 8 that failed strictly (section 4.3). Selection rule: all
Excel-to-PowerPoint and Word-to-PowerPoint L4 tasks whose primary artefact is
a deck or a deck plus workbook, two L3 deck workflows that exercise ordering
and chart rebuilding, one v1 L3 deck workflow with a locked reference slide,
and two L1 atomic PPTX tasks as a sanity control.

| task | level | formats | why |
|---|---|---|---|
| `atomic__ppt_004_slide_reorder_seed` | L1 | pptx | control: pure slide reorder |
| `atomic__ppt_005_table_structure_seed` | L1 | pptx | control: insert a table column |
| `single_doc_workflow__pptwf_001_board_deck_locked_layout_finalize_seed` | L3 | pptx | draft cleanup with a locked reference slide and in-deck ordering cues |
| `docops_v2_l3_029_pptx_qbr_release_deck` | L3 | pptx | 17-step QBR release flow: delete, reorder, rebuild agenda/KPI/risk/mitigation tables, notes, footers |
| `docops_v2_l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | pptx | corrections log applied before rebuilding a native chart and tables; style migration |
| `cross_doc_docops__pptxr_001_monthly_board_pack_refresh_locked_layout_seed` | L4 | xlsx+docx to pptx | metric tiles and action table from two workbooks, duplicate a locked layout |
| `cross_doc_docops__pptxr_004_handover_owner_matrix_from_closeout_logs_seed` | L4 | xlsx+docx to pptx | metrics and owner matrix from closeout logs |
| `docops_v2_l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | pptx+xlsx | finance exception notice overrides draft deck; PPTX tables and new XLSX register must agree; formulas and validation preserved |
| `docops_v2_l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | xlsx+pptx | public/internal boundary across deck and tracker; native tables, formulas, validation |
| `docops_v2_l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | pptx+xlsx (from docx/pdf/xlsx) | closest analogue to a financing deck: rate rules, caps, totals computed in a workbook and summarised on slides |
| `docops_v2_l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | pptx+xlsx | public deck plus internal workbook that must agree on public slots |
| `docops_v2_l4_065_word_ppt_shortlist_interview_package_style` | L4 | docx+pptx | Word-to-slides with a style brief and confidentiality boundary |

Not chosen: `l4_059` and `l4_062` (poster/signage style packs, same shape as
`l4_060`), `l4_056` (deck to Word memo) and `l4_057` (deck to PDF proof),
which do not involve a workbook.

## 4. Results

Strict reward is 1 only when every test function of the task's verifier passes (this is what `tests/test.sh` writes to `reward.txt`). "tests" is passed/total test functions; v1 tasks have a single function. "lenient" re-runs the same verifier after mapping the verifier's expected file names onto the files the agent actually wrote, and is shown only where that mapping was needed. "verifier mentions" counts transcript lines that reference `tests/`, `test_outputs`, `verifier_utils` or `verifier_expectations`; it is 0 for every main run. Per-test outcomes and the first failing assertion for every run are in `results.json`.

### 4.1 All main runs

| task | level | skills | model | strict reward | tests | lenient reward | lenient tests | wall s | turns | tool calls | outputs open | verifier mentions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `atom:ppt_004_slide_reorder` | L1 | off | claude-sonnet-5-5 | **1** | 1/1 | - | - | 9 | 3 | 2 | yes | 0 |
| `atom:ppt_004_slide_reorder` | L1 | on | claude-sonnet-5-5 | **1** | 1/1 | - | - | 10 | 3 | 2 | yes | 0 |
| `atom:ppt_005_table_structure` | L1 | off | claude-sonnet-5-5 | **1** | 1/1 | - | - | 12 | 3 | 2 | yes | 0 |
| `atom:ppt_005_table_structure` | L1 | on | claude-sonnet-5-5 | **1** | 1/1 | - | - | 15 | 6 | 4 | yes | 0 |
| `wf:pptwf_001_board_deck_locked_layout_finalize` | L3 | off | claude-sonnet-5-5 | **0** | 0/1 | - | - | 19 | 5 | 4 | yes | 0 |
| `wf:pptwf_001_board_deck_locked_layout_finalize` | L3 | on | claude-sonnet-5-5 | **0** | 0/1 | - | - | 15 | 3 | 2 | yes | 0 |
| `v2:l3_029_pptx_qbr_release_deck` | L3 | off | claude-sonnet-5-5 | **1** | 1/1 | - | - | 30 | 4 | 3 | yes | 0 |
| `v2:l3_029_pptx_qbr_release_deck` | L3 | on | claude-sonnet-5-5 | **1** | 1/1 | - | - | 33 | 7 | 5 | yes | 0 |
| `v2:l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | off | claude-sonnet-5-5 | **0** | 6/7 | - | - | 30 | 3 | 2 | yes | 0 |
| `v2:l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | on | claude-sonnet-5-5 | **0** | 6/7 | - | - | 39 | 7 | 5 | yes | 0 |
| `xdoc:pptxr_001_monthly_board_pack_refresh_locked_layout` | L4 | off | claude-sonnet-5-5 | **0** | 0/1 | - | - | 24 | 4 | 3 | yes | 0 |
| `xdoc:pptxr_001_monthly_board_pack_refresh_locked_layout` | L4 | on | claude-sonnet-5-5 | **0** | 0/1 | - | - | 25 | 7 | 5 | yes | 0 |
| `xdoc:pptxr_004_handover_owner_matrix_from_closeout_logs` | L4 | off | claude-sonnet-5-5 | **1** | 1/1 | - | - | 22 | 5 | 4 | yes | 0 |
| `xdoc:pptxr_004_handover_owner_matrix_from_closeout_logs` | L4 | on | claude-sonnet-5-5 | **1** | 1/1 | - | - | 29 | 8 | 6 | yes | 0 |
| `v2:l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 0 | 3/4 | 30 | 4 | 3 | yes | 0 |
| `v2:l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | on | claude-sonnet-5-5 | **0** | 0/4 | 0 | 3/4 | 36 | 4 | 3 | yes | 0 |
| `v2:l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 43 | 5 | 4 | yes | 0 |
| `v2:l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | on | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 49 | 5 | 4 | yes | 0 |
| `v2:l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | off | claude-sonnet-5-5 | **0** | 0/5 | 0 | 1/5 | 74 | 8 | 7 | yes | 0 |
| `v2:l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | on | claude-sonnet-5-5 | **0** | 0/5 | 0 | 1/5 | 87 | 12 | 9 | yes | 0 |
| `v2:l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 38 | 5 | 4 | yes | 0 |
| `v2:l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | on | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 51 | 12 | 9 | yes | 0 |
| `v2:l4_065_word_ppt_shortlist_interview_package_style` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 0 | 2/4 | 42 | 4 | 3 | yes | 0 |
| `v2:l4_065_word_ppt_shortlist_interview_package_style` | L4 | on | claude-sonnet-5-5 | **0** | 0/4 | 0 | 2/4 | 52 | 12 | 9 | yes | 0 |

### 4.2 Pass rate by level

| level | skills | tasks | strict pass | lenient pass |
|---|---|---|---|---|
| L1 | off | 2 | 2/2 | 2/2 |
| L1 | on | 2 | 2/2 | 2/2 |
| L3 | off | 3 | 1/3 | 1/3 |
| L3 | on | 3 | 1/3 | 1/3 |
| L4 | off | 7 | 1/7 | 3/7 |
| L4 | on | 7 | 1/7 | 3/7 |

### 4.3 Opus reruns of the strict failures (skill-off)

| task | level | skills | model | strict reward | tests | lenient reward | lenient tests | wall s | turns | tool calls | outputs open | verifier mentions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `wf:pptwf_001_board_deck_locked_layout_finalize` | L3 | off | claude-sonnet-5-5 | **0** | 0/1 | - | - | 19 | 5 | 4 | yes | 0 |
| `wf:pptwf_001_board_deck_locked_layout_finalize` | L3 | off | claude-opus-5-5 | **1** | 1/1 | - | - | 37 | 6 | 5 | yes | 0 |
| `v2:l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | off | claude-sonnet-5-5 | **0** | 6/7 | - | - | 30 | 3 | 2 | yes | 0 |
| `v2:l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | off | claude-opus-5-5 | **0** | 6/7 | - | - | 883 | 11 | 9 | yes | 2 |
| `xdoc:pptxr_001_monthly_board_pack_refresh_locked_layout` | L4 | off | claude-sonnet-5-5 | **0** | 0/1 | - | - | 24 | 4 | 3 | yes | 0 |
| `xdoc:pptxr_001_monthly_board_pack_refresh_locked_layout` | L4 | off | claude-opus-5-5 | **0** | 0/1 | - | - | 54 | 7 | 6 | yes | 0 |
| `v2:l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 0 | 3/4 | 30 | 4 | 3 | yes | 0 |
| `v2:l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | off | claude-opus-5-5 | **0** | 0/4 | 1 | 4/4 | 86 | 7 | 6 | yes | 0 |
| `v2:l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 43 | 5 | 4 | yes | 0 |
| `v2:l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | off | claude-opus-5-5 | **0** | 0/4 | 0 | 3/4 | 123 | 12 | 11 | yes | 0 |
| `v2:l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | off | claude-sonnet-5-5 | **0** | 0/5 | 0 | 1/5 | 74 | 8 | 7 | yes | 0 |
| `v2:l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | off | claude-opus-5-5 | **0** | 0/5 | 0 | 1/5 | 243 | 13 | 12 | yes | 0 |
| `v2:l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 1 | 4/4 | 38 | 5 | 4 | yes | 0 |
| `v2:l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | off | claude-opus-5-5 | **0** | 0/4 | 1 | 4/4 | 127 | 10 | 9 | yes | 0 |
| `v2:l4_065_word_ppt_shortlist_interview_package_style` | L4 | off | claude-sonnet-5-5 | **0** | 0/4 | 0 | 2/4 | 42 | 4 | 3 | yes | 0 |
| `v2:l4_065_word_ppt_shortlist_interview_package_style` | L4 | off | claude-opus-5-5 | **0** | 0/4 | - | - | 69 | 4 | 3 | NO | 1 |

Opus reruns were requested by the orchestrator for every task that failed
strictly in the main batch, skill-off only, same 900 s cap. Model
`claude-opus-5-5` was accepted by the CLI (`--model claude-opus-5-5`) and is
the model recorded in every opus run's transcript. Observations:

* `pptwf_001` (board deck, in-deck ordering cues): **opus passed** on its
  single attempt, where Sonnet passed 1 of 4.
* `pptxr_001` (board pack refresh): **opus failed with the identical slide
  order** as every Sonnet attempt. See section 5.0.
* `l3_026`: opus took 883 s (near the cap, one API turn stalled for about
  12 minutes), read the shipped `task_metadata.json` and built the deck from
  its `verifier_expectations` (2 transcript lines flagged), and still failed
  one hidden term (`Aptos` on the style-guide slide). Treat as contaminated
  and uninformative.
* `l4_058`: strict 0/4 for the file-name reason; **lenient 4/4**. Opus wrote
  a `Status` header where Sonnet kept `Risk`, which was Sonnet's only content
  miss.
* `l4_043`: lenient 3/4. Opus over-applied the public/internal boundary and
  replaced the internal evidence text for E-21A inside the *internal*
  tracker workbook with "Internal investigation record (internal only)";
  the verifier (and the source evidence index) expect the original
  "Unblinded lot investigation notes". Sonnet got this right in both modes.
* `l4_060`: lenient 4/4, same as Sonnet.
* `l4_061`: lenient 1/5, same as Sonnet, failing on the same hidden schema and
  unreconciled constant; opus also computed $6,712.90.
* `l4_065`: **not run.** The CLI returned "You've hit your org's monthly spend
  limit" before the agent made any edit; no output exists. The row is kept
  in `results.json` with `status` set accordingly.

Opus runs took 1.5 to 3 times longer than the Sonnet runs of the same tasks.
Net effect of the stronger tier on the sampled failures: one ordering task
fixed (`pptwf_001`), one header fixed (`l4_058`), one new content error
introduced (`l4_043`), and the repeat ordering failure (`pptxr_001`) and all
benchmark-defect failures unchanged.

## 5. Analysis

### 5.0 The board-pack slide-order failure (5 attempts, 2 models, identical result)

`cross_doc_docops__pptxr_001_monthly_board_pack_refresh_locked_layout_seed`
is the one task where every attempt, on both models, failed the same way.
Because it is also the purest "workbook to board deck" task in the sample, it
deserves the full record.

**Instruction (verbatim, `instruction.md`):**

> Refresh the metric tiles and action table, insert a `Decision Snapshot`
> slide by duplicating the locked reference layout, place it before
> `Closing`, and keep the reference slide unchanged.
>
> Notes: Keep the reference slide unchanged. Do not rebuild the inserted
> slide with a different layout.

Supporting inputs: `metrics.xlsx` (Open Actions 5, Late Items 2, Completed 8),
`action_log.xlsx` (two rows: Mia Torres / Release FAQ / 2025-02-14, Devin Park
/ Post packet / 2025-02-15), `decision_note.docx` (three decisions).

**Input deck (5 slides):** 1 Monthly Board Pack; 2 Metrics with `[Fill]`
tiles; 3 Action Tracker, whose body text reads *"Keep this live table after
the inserted decision slide."*; 4 Closing; 5 Layout Reference - Decision Card
(three `[Fill]` decision lines and the note "Reference slide; duplicate this
layout for the inserted decision slide").

**What the verifier checks** (`verify_ppt` in `tests/test_outputs.py`, driven
by `verifier_expectations`): exact slide-title order `Monthly Board Pack,
Metrics, Decision Snapshot, Action Tracker, Closing, Layout Reference -
Decision Card`; required lines on Metrics and Decision Snapshot; the three
action-table cells; that the reference slide's text, notes, shape count and
picture count equal the input; and that the Decision Snapshot's shape count,
picture count, title signature and first-body signature equal the reference
slide's (i.e. it really is a duplicate, not a rebuilt slide).

**What the agents did, every time:** filled the three metric tiles correctly,
filled the action table correctly, duplicated the reference slide at the XML
level (so the signature checks pass), filled the three decisions correctly,
left the reference slide untouched, and then inserted the new slide
immediately before Closing, producing `Monthly Board Pack, Metrics, Action
Tracker, Decision Snapshot, Closing, Layout Reference`. The only assertion
that fails is the slide order, at index 2 (we re-ran every later check of the
verifier by hand on the three recorded runs; all pass). This happened in: the two
discarded Sonnet batches, the skill-off main run, the skill-on main run
(where the agent rendered thumbnails of the result and declared it
correct), and the opus rerun. In the skill-off main run the agent had
printed the full XML of slide 3, including the sentence "Keep this live
table after the inserted decision slide", before editing.

**Reading:** the brief says "before Closing" and the agents satisfied the
brief literally. The deck says "after the inserted decision slide" on the
Action Tracker, which resolves the ambiguity, and no agent integrated it.
This is the failure mode to design for in a financing-deck task: placement
rules that live in the artefact (template notes, slide-body instructions,
"appendix follows the ask" conventions) rather than in the prompt, and that
a thumbnail check cannot reveal because every slide looks right in
isolation.

### 5.1 Three benchmark-side problems that dominate the L4 numbers

Before classifying agent failures, three properties of the public DocOps
package need to be on the table, because they explain most of the strict
L4 zeros above.

**(a) Every v2 L4 task names its deliverables differently in `instruction.md`
and in the verifier.** We checked all 40 `docops_v2_l4_*` tasks: in 40 of 40
the file names under "Required Outputs" in the instruction (for example
`renewal_action_register.xlsx` and `..._input.pptx`) differ from the names the
verifier opens (`..._register.xlsx` and `..._deck.pptx`). The 170 other tasks
are consistent. Inside the Harbor container only one of the two expected
names is exposed, as the `OUTPUT_PATH` environment variable, and nothing
tells the agent to look there; none of our 24 runs did. Consequently an
agent that follows the instruction to the letter scores 0 on all four
test functions of these tasks, including `test_outputs_exist`. Our
"lenient" column re-runs the same verifier after pointing it at the file
the agent actually wrote (only when exactly one file of the right extension
exists). We report both; the strict number is what the official harness
would produce.

**(b) Several v2 verifiers check a hidden schema that no input specifies.**
Examples we hit: `l4_061` requires sheet names `Project Summary`,
`Measure Calculations`, `Raw Inputs`, `Program Rules`, table names such as
`tblMeasureCalculations`, the exact formula text `=C3*615` for VFD kWh (the
615 kWh/hp factor appears in none of the six inputs) and the literal string
`$7,254.53` on a slide, which does not reconcile with the verifier's own
formulas (0.08 x (32,140.8 + 6,770.4) + 30 x 120 = $6,712.90, the value the
agent computed in both modes). `l4_065` requires Word headings `Interview
Storyline`, `Core Team Roles`, `Landscape Project Sheets`, `Closeout and
Handoff`, whereas the draft document the agent is told to edit has
`Team` and `Projects`. `l3_026` requires the word `accent` on the
"Publication Style Guide" slide. These tasks cannot be passed from the
inputs; they measure whether the agent guesses the authors' schema.

**(c) 33 v2 L3 tasks ship the verifier's expected values into the agent's
container.** Their Dockerfiles `COPY task_metadata.json /root/`, and that
file contains `verifier_expectations` (slide titles, required strings,
colours, chart values). `l3_026` is one of them. Our agent did not open the
file in any run (we checked the transcripts), but a less scrupulous agent
could. We flag it as a contamination risk for any published L3 number.

### 5.2 Per-task failure modes

Classification key: **LRS** long-range state tracking, **SV** shallow
verification (claimed done but wrong), **DE** destructive edit of structure
or metadata, **NUM** numeric or formula error, **TL** tooling limitation,
**BENCH** benchmark defect (not an agent failure). "Confirmed on" counts
attempts with the same outcome, including the two earlier batches that we
discarded for harness reasons (see Caveats) when the failing check was
identical.

* **`single_doc_workflow__pptwf_001` (L3, board deck finalize)**, fail in
  both modes, confirmed on 3 of 4 Sonnet attempts (1 pass), opus pass.
  **LRS.** The input deck starts with the locked reference slide, and the
  instruction says to "restore the live slide order from Board Memo through
  the locked reference slide". The deck itself carries the cues ("Keep the
  closing slide at the end of the live storyline", "Keep this live table
  after the inserted decision slide"). The agent removed the draft markers
  and the parking-lot slide correctly every time, but placed the reference
  slide in a different position on each attempt (after Decision Snapshot;
  before Closing; last). It never re-read the in-slide cues after editing.
  Everything else in the deck was right. Financing-deck relevance: direct.
  A locked reference or template slide that must stay last, plus
  in-document ordering rules, is the normal shape of a template-driven
  deck.

* **`cross_doc_docops__pptxr_001` (L4, Excel metrics and action log to board
  pack)**, fail in both modes, confirmed on 4 of 4 Sonnet attempts and 1 of 1 opus attempt; see 5.0.
  **LRS.** Metric tiles, the action table and the duplicated decision card
  were all correct; the only failure is slide order (details in 5.0). The instruction says to
  insert the new Decision Snapshot "before Closing"; the agent put it
  immediately before Closing, after the Action Tracker, while the Action
  Tracker slide itself says "Keep this live table after the inserted decision
  slide". The cue was in front of the agent: in the skill-off run it dumped
  the raw XML of every slide to the terminal before editing, and still acted
  on the instruction's literal "before Closing". This is the same
  cue-in-the-document failure as above and it survived four attempts and the
  skill. Financing-deck relevance: direct.
  Workbook-to-slides refreshes commonly contain "keep X after Y" rules in the
  deck rather than in the brief.

* **`docops_v2_l3_026` (L3, chart rebuild)**, 6/7 tests in both modes;
  earlier two attempts passed 7/7. Skill-off failed because the Transition
  Action Plan was rebuilt as bullets rather than a native table (the
  instruction says "rebuild ... transition actions" without saying table;
  the verifier demands a table). Skill-on failed because the Publication
  Style Guide slide was left with only a title and footer. **SV** for the
  skill-on run (the agent reported the deck complete without checking that
  every required slide had body content), **BENCH** for the table
  requirement. The clustered column chart with the corrected values, the
  corrections log, note cleanup and style migration all passed in every
  attempt. Financing-deck relevance: partial; chart data correctness, which is
  what matters for a financing deck, was never the problem.

* **`docops_v2_l4_058` (L4, QBR risk table and action register, PPTX+XLSX)**,
  strict 0/4 (**BENCH**, file names), lenient 3/4 in both modes. The one
  real miss: the risk table kept the draft deck's `Risk` column header, and
  the verifier looks for a `Status` column (the instruction says the three
  tables "must agree exactly on account, owner, action, and status"). Because
  pytest stops at the first assertion we re-ran the remaining checks of that
  test function by hand: slide order, scratch-slide removal, executive
  summary wording with the finance overrides (Northstar Bank to Watch, Zenith
  Foods to $1.40M), the action-register slide, the risk callout and both
  reference slides all pass, as do the workbook's native table, hidden Rules
  sheet, defined name, data validation, live `OK` formulas and the
  PPTX-to-XLSX consistency test. **SV**, borderline. Financing-deck relevance: direct. This is the
  "authoritative override from a finance notice must propagate into every
  table" pattern, and the agent got the numbers right in both documents.

* **`docops_v2_l4_043` (L4, CAPA tracker and public deck, XLSX+PPTX)**,
  strict 0/4 (**BENCH**), lenient 4/4 in both modes. Public/internal
  boundary, owner alias expansion, status values, native tables with exact
  refs, formulas, data validation, hidden sheet, defined names and
  cross-document consistency were all correct. Not an agent failure.

* **`docops_v2_l4_060` (L4, signage deck and run-of-show workbook)**, strict
  0/4 (**BENCH**), lenient 4/4 in both modes. Same picture as `l4_043`.

* **`docops_v2_l4_061` (L4, utility rebate M&V deck and calculation tracker)**,
  strict 0/5 (**BENCH**), lenient 1/5. The agent's eligibility logic,
  exclusions, kWh and incentive arithmetic, 50% cap and privacy boundary
  were correct and its workbook used live formulas that recalculated in
  LibreOffice; it failed on the hidden sheet/table/title schema and on a
  verifier constant that does not reconcile with the inputs (section 5.1b).
  We classify this as **BENCH**, with one genuine agent-side observation:
  neither run put the required six slide titles on the deck, because the
  instruction says "six-slide PPTX summary" and the titles are only in the
  verifier. Financing-deck relevance: this is the closest task in DocOps to
  a workbook-to-slides financing deck (rates, caps, totals that must agree
  across workbook and slides). The agent reconciled the numbers; the
  benchmark did not.

* **`docops_v2_l4_065` (L4, Word leave-behind and interview deck)**, strict
  0/4 (**BENCH**), lenient 2/4. Cross-output role/project consistency and
  the PX-31 exclusion passed. The Word check fails on the hidden heading
  schema (5.1b); the PPT check fails because the title slide must contain
  the three words "shortlist", "interview" and "deck" and the agent wrote
  "Shortlist Interview". Both **BENCH**. Note that in the discarded first
  batch this task "passed" only because the agent found and read
  `tests/test_outputs.py`, which is why that batch was thrown away.

### 5.3 What skills changed

Nothing in the pass/fail outcome. In skill-on runs the agent invoked a
DocOps skill through the Skill tool in 8 of 12 runs and read or ran skill
files in 10 of 12 (`thumbnail.py` to render the deck in 10 runs,
`unpack.py`/`pack.py` in 10). Skill-on runs took 0.8 to 1.3 times the wall
time of the matching skill-off run and up to 3 times more turns, and produced
the same strict and lenient results on every task. Rendering slides to images
was not unique to skill-on: the skill-off agent on `l4_061` converted its deck
with LibreOffice, tiled the PNGs, looked at them and fixed a mis-aligned table
cell. Neither mode's visual check caught the failures that mattered (slide
order, hidden schema), because those are not visible in a thumbnail.

### 5.4 Top failure patterns, ranked by what they would do to a financing-deck task

1. **Benchmark specification drift (file names, hidden schema, unreconciled
   constants).** Dominates the v2 L4 numbers. For our own benchmark the
   lesson is procedural: the instruction, the environment variables and the
   verifier must be generated from one source of truth, and every numeric
   constant in a verifier must be derivable from the inputs. We should also
   not ship expectations into the agent's container.
2. **Ordering and placement rules stated inside the document rather than in
   the brief (LRS).** Both genuine, repeatable failures were of this kind.
   A financing deck has exactly these rules (appendix after the ask slide,
   reference slide stays last, "sources" slide after every chart). The agent
   reads supporting files diligently but does not re-read every live slide's
   text after it has started editing.
3. **Schema-level consistency between workbook and deck (SV).** The
   `Risk`-vs-`Status` header miss on `l4_058` is small but it is the kind of
   thing that breaks a reconciliation check across documents. Numbers
   themselves were never wrong in any run (no NUM failures), and no run
   produced a file that failed to open or lost structure (no DE or TL
   failures): every pptx/xlsx/docx written in 24 runs opened with
   python-pptx/openpyxl/python-docx and passed a zip integrity check.

## 6. Reproduction

Everything below was run as root in one container; adjust `BENCH` paths in
`tools/run_task.py` if you use another location. The harness scripts in
[`tools/`](tools/) are the exact files used.

```bash
# 0. environment: Python 3.13, LibreOffice, Claude Code CLI authenticated, Docker NOT required
mkdir -p /home/user/bench && cd /home/user/bench
git clone --depth 1 https://github.com/icip-cas/DocOps.git        # commit ccf7a75 at time of writing
python3 -m venv venv
grep -v harbor DocOps/requirements.txt > reqs.txt                  # vendored Harbor is not needed outside Docker
./venv/bin/pip install -r reqs.txt markitdown pytest-json-report
./venv/bin/python -I DocOps/scripts/verify_package.py              # expects 210 tasks, L1 50 / L2 40 / L3 60 / L4 60
cp -r <this directory>/tools /home/user/bench/tools
./venv/bin/python -I tools/inventory.py DocOps/tasks inventory.json # inventory.md was rendered from this

# 1. one task, one mode (off|on). Agent cap 900 s (AGENT_TIMEOUT), CLI default model unless DOCOPS_MODEL is set.
./venv/bin/python -I tools/run_task.py docops_v2_l4_058_ppt_xlsx_qbr_readout_and_action_register off
# -> runs/<task>__skill_off/{work/submission/*, claude-code.jsonl, tests/, pytest_output.txt, pytest_report.json, summary.json}

# 2. the 12-task batches, strictly sequential (see Caveats for why)
./tools/run_batch.sh off 1 && ./tools/run_batch.sh on 1

# 3. opus reruns of the strict failures (tasks listed in tools/failed_tasks.txt)
DOCOPS_MODEL=claude-opus-5-5 ./tools/run_opus.sh

# 4. lenient regrade (file-name remap only) and the tables/results.json used in this README
./venv/bin/python -I tools/regrade_lenient.py
./venv/bin/python -I tools/report.py            # writes results.json and results_tables.md

# 5. regrade an existing run without re-running the agent
./venv/bin/python -I tools/run_task.py <task> off grade
```

The nested Claude Code invocation used by `run_task.py` is, for skill-off:

```bash
CLAUDE_CONFIG_DIR=<fresh dir> IS_SANDBOX=1 INPUT_PATH=... OUTPUT_PATH=... TASK_ID=... DOC_TYPE=... \
claude --verbose --output-format stream-json --permission-mode bypassPermissions \
       --setting-sources project --strict-mcp-config --disable-slash-commands \
       [--model claude-opus-5-5] --print -- "<instruction.md with /root/ rewritten to the work dir>"
```

and the same without `--disable-slash-commands` plus `<workdir>/.claude/skills/`
= DocOps `skills/` for skill-on. `CLAUDE_CODE_SYNC_SKILLS` is removed from the
environment so the hosting session's skills do not leak in.

## 7. Caveats

* **Not Docker.** Runs happened directly on the host, not in the
  `harbor-claude-code-base:2.1.114` image, so the agent saw a richer
  toolchain (LibreOffice, Node, the full venv) and a different path prefix
  (`/home/user/bench/live/<run>/work/` instead of `/root/`). Verifier logic
  was unchanged apart from rewriting `/root/` and `/tests/` prefixes in
  `task_metadata.json`, `test_outputs.py` and `verifier_utils.py`.
* **Model.** The CLI default here is `claude-sonnet-5-5`, not the
  `claude-sonnet-4-6` that DocOps' wrapper defaults to. The model is recorded
  per run in `results.json` (`agent_model_from_transcript`, taken from the
  assistant messages in each run's `claude-code.jsonl`). Opus reruns used
  `--model claude-opus-5-5`.
* **Two discarded batches.** Our first batch ran three tasks in parallel and
  copied every file from `environment/` into the work dir, including
  `task_metadata.json` for tasks whose Dockerfile does not ship it; it was
  stopped after we saw an agent read it. The second batch was sequential but
  placed `tests/` beside the work directory; one agent (`l4_065`) found and
  read the verifier, so the whole batch was discarded and the harness changed
  to materialise `tests/` only after the agent exits (as Harbor does). Every
  reported run has `transcript_verifier_mentions = 0`, except where noted
  for the opus rerun of `l3_026`, whose Dockerfile legitimately ships the
  expectations file (section 5.1c). Outcomes from the discarded batches are
  used only for the "confirmed on N attempts" statements in section 5.2.
* **Single sample per cell.** Each task/mode cell is one run. We observed
  run-to-run variance on two tasks (`pptwf_001`: 1 pass in 4 Sonnet
  attempts; `l3_026`: 2 full passes in 4 attempts), so treat single-cell
  differences between skill-on and skill-off as noise.
* **Strict vs lenient.** The lenient column changes only the file name the
  verifier opens, never the checks. It is applied only when exactly one file
  of the expected extension exists in `submission/`.
* **Sequential execution.** With three agents in parallel the agent wrote
  `cd /home/user/bench/runs/*/work`, a glob that matched sibling runs.
  Sequential runs with a single `live/` directory remove that risk, at the
  cost of wall time (the whole 24-run batch still took about 15 minutes;
  the longest single run was 87 s, far under the 900 s cap, so the cap never
  bound).
* **No published per-task numbers to compare against.** The project page
  and arXiv were unreachable from this environment.
* **Cost not recorded.** The CLI reports `total_cost_usd = 0` under this
  account's billing, so no cost column is given.

## 8. Files

| file | content |
|---|---|
| `README.md` | this report |
| `results.json` | one record per run: task, level, mode, model, per-test outcomes with first failing message, lenient regrade, wall time, turns, tool calls, which input files were materialised, env exported, verifier-mention count |
| `inventory.md` | all 210 tasks with level, format, number of deliverables and summary |
| `tools/run_task.py` | materialise + run agent + grade one task |
| `tools/run_batch.sh`, `tools/run_opus.sh` | batch drivers |
| `tools/regrade_lenient.py` | file-name remap regrade |
| `tools/report.py` | builds `results.json` and the markdown tables |
| `tools/inventory.py` | builds the inventory |
| `tools/failures.py`, `tools/show.py`, `tools/collect.py` | inspection helpers |

Benchmark data and output documents are deliberately not committed.
