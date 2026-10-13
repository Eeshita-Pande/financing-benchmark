# PPT-Eval baseline with Claude Code (CLI track)

**Status: blocked at the data step. No benchmark task ran.** The 12 source
decks live on archive.org, which this session's network policy denies. This
directory still delivers the full 120-task inventory, the failing set with a
rubric-level analysis, a working end-to-end harness (agent + grader + Claude
judge) validated on a synthetic deck, and exact reproduction commands for when
the decks are available. Nothing in `results.json` is a benchmark score.

Benchmark: [microsoft/ppteval](https://github.com/microsoft/ppteval)
(ICML 2026, 120 PowerPoint tasks on 12 decks). Pinned commits: `main`
`1b8b55a2`, `gh-pages` `aa930cc9`.

## 1. Blocker

| Need | Host | Result |
|---|---|---|
| 12 source `.pptx` (`data/files/PowerPoint/files.txt`) | `archive.org`, `s3.us.archive.org`, `ia*.us.archive.org` | CONNECT 403 (policy denial) |
| Wayback fallback | `web.archive.org` | CONNECT 403 |
| Website with results | `microsoft.github.io` | CONNECT 403 (worked around: cloned the `gh-pages` branch over git) |
| Alternative mirrors | `huggingface.co`, `hf-mirror.com` | CONNECT 403 |
| Forks that might vendor the decks | `github.com` HTML and REST API | 403 for repos not attached to the session; only git smart-HTTP works |

Fix: add `archive.org` and `s3.us.archive.org` under Allowed domains in the
environment's network settings, or drop the 12 decks into
`data/files/PowerPoint/` by hand. Two further caveats apply once the files
are present:

- The repo's `hydrate_data.py` round-trips each deck through PowerPoint Online
  to normalise metadata. That step needs a OneDrive account and is skipped
  here, so the "no extraneous changes" rubric nodes (which diff the agent's
  output against the original) may penalise python-pptx re-save artefacts.
- The repo pins the VLM judge through litellm (`RUBRIC_DEFAULT_LLM`). No API
  key exists here, so `scripts/claude_judge.py` routes `vlm_call`/`llm_call`
  through the local `claude -p` CLI. Any VLM node scored that way must be
  labelled **Claude-judged**.

## 2. Inventory

120 tasks, 10 per deck. Full table (file, tier, kind, rubric leaf counts,
goal) is in [`inventory.md`](inventory.md).

| Tier | Tasks | Edit / Create | Tasks with VLM rubric nodes |
|---|---|---|---|
| Easy | 51 | 33 / 18 | 19 |
| Medium | 39 | 19 / 20 | 21 |
| Hard | 30 | 15 / 15 | 21 |

| File | Easy | Medium | Hard |
|---|---|---|---|
| 3.pptx (OS lecture) | 5 | 2 | 3 |
| 4._Pre-Colonial_Filipino_Culture.pptx | 4 | 4 | 2 |
| Accounting Equation.pptx | 3 | 3 | 4 |
| Aircraft_surface.pptx | 8 | 1 | 1 |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | 5 | 5 | 0 |
| HSC Careers and Expo FINAL COM MOD.pptx | 3 | 3 | 4 |
| Jean-Nicolas-Louis Durand.pptx | 6 | 1 | 3 |
| Obesity.pptx | 2 | 6 | 2 |
| Revisiting Classical  Social Experiments [Autosaved].pptx | 5 | 2 | 3 |
| Worms.pptx | 3 | 5 | 2 |
| application+layer+slide.pptx | 4 | 3 | 3 |
| pediatic glasses when to prescribe1.pptx | 3 | 4 | 3 |

Rubric mechanics (from `ppteval/verify/ppt/verifier.py` and `ai-rubric`):
each task has a tree of leaf scorers that are Python functions run with
`original_ppt_path`, `modified_ppt_path`, a `ppt_diff` object
(animations, transitions, slide add/remove/modify) and rendered slide
screenshots. Critical leaves gate the score; non-critical leaves carry weight
0.3. Success is `score == 1.0`. 61 of 120 tasks contain at least one
`vlm_call` leaf, 2 tasks use `llm_call` only, and the remaining 57 are fully
deterministic.

## 3. Published results and the failing set

Only tier-level numbers are published (`_data/benchmark.yml` on `gh-pages`,
Table 1 of the paper). No per-task results exist in the repo or the site.

| Agent | Overall SR / Avg | Hard SR / Avg |
|---|---|---|
| Human baseline | 80 / 90 | 68 / 88 |
| GPT-5.5 (Medium) | 63 / 78 | 41 / 67 |
| API baseline (Claude-4.5-Opus, file-level) | 62 / 81 | 30 / 61 |
| Claude-Opus-4.8 (High) | 62 / 78 | 41 / 67 |
| Claude-4.5-Opus | 45 / 57 | 35 / 48 |
| Claude-4-Sonnet | 42 / 53 | 17 / 33 |
| Computer-Use-Preview | 38 / 49 | 20 / 36 |
| OpenCUA-32B | 28 / 42 | 11 / 28 |

The 30 Hard-tier tasks are therefore the failing set. The best GUI agents
solve about 4 in 10 of them; humans solve about 7 in 10. Grouped by what the
rubric demands:

| Group | Tasks | What the rubric checks |
|---|---|---|
| Layout re-flow (two/three columns, layout switch) | Accounting Equation-008, HSC-038, Obesity-020, pediatic-035 | Layout name via python-pptx, text in separate placeholders, VLM for column arrangement |
| Build a table / chart / SmartArt / flowchart from slide content | Accounting Equation-015, -045, Obesity-015, pediatic-032, HSC-072, Worms-060, Revisiting-016, 4._Pre-Colonial-005 | Object type present, headers/rows match source text, VLM for semantics and size |
| Draw or replace diagrams | 3-007, 3-030, application+layer-011, -019, Revisiting-018 | Almost entirely VLM: presence, sequence, colour, spacing |
| Image geometry (resize, crop, rotate, overlay) | Jean-Nicolas-Louis Durand-008, -015, -025, 3-009, Aircraft_surface-004 | Exact EMU ratios / rotation attribute, VLM for crop content and overlap |
| Formatting consistency / theme | 4._Pre-Colonial-020, pediatic-019, Accounting Equation-012 | Footer placeholder on every slide with centred alignment; VLM for consistency and preserved colours |
| Hyperlinks and positioned text | HSC-064, Revisiting-033, Worms-007, HSC-022, application+layer-021 | `hlinkClick` targets (slide `jump` vs URL), text box position relative to a diagram word (VLM) |

## 4. Planned run set (12 tasks, not executed)

Hard-tier editing tasks on charts, tables, layout and formatting, spread over
9 of the 12 decks. These are the commands that would have run; the rubric
risk notes are derived from reading the rubric code, not from observed runs.

| Task | Deck | Goal (short) | Main rubric risk for a CLI agent |
|---|---|---|---|
| 3-009 | 3.pptx | Tint the slide 4 figure blue via a semi-transparent overlay | Single VLM critical node judges "light blue tone"; python-pptx has no transparency API, so the agent must write raw `<a:alpha>` XML. Non-critical node demands exactly one new shape. |
| 4._Pre-Colonial_Filipino_Culture-020 | Filipino Culture | Make list items 4-5 match items 1-3 | Requires perceiving which run-level properties differ (font, size, bullet, indent). Text content on slide 12 must be byte-identical afterwards. |
| Accounting Equation-008 | Accounting Equation | Switch slide 6 to "Two Content" and split Assets / Liabilities | Deterministic: layout name must be exactly "Two Content" and the two terms must land in different placeholders. Re-layout in python-pptx leaves orphan placeholders that trip the extraneous-change node. |
| Accounting Equation-012 | Accounting Equation | Centred footer on every slide | Three critical deterministic nodes: footer placeholder on all slides, exact text, centred alignment. Footer placeholders are usually absent from slides and must be instantiated from the layout. |
| Aircraft_surface-004 | Aircraft_surface | Append a bullet and shrink the image to avoid overlap | Exact bullet text and last-position checks plus "image resized" and a VLM overlap check. Agents often resize without re-reading the geometry. |
| HSC-038 | HSC Careers | Render the slide 8 checklist in two columns | VLM-only critical node; text must stay identical; animations on slide 8 must not change (checklist slides often carry per-paragraph animations that break when paragraphs move). |
| HSC-072 | HSC Careers | Convert the slide 8 checklist to a 2-column table | Deterministic: rows must contain the original items and the text box must not simply be duplicated. |
| Jean-Nicolas-Louis Durand-008 | Durand | Shrink the slide 4 image by 20 % keeping aspect ratio | Pure geometry: width and height both at about 80 % of original EMU; identifying which picture is "the historical document" needs rendering. |
| Obesity-020 | Obesity | Two-column Adults / Children comparison with bullets re-sorted | Four VLM critical nodes (headers, left/right order, bullets moved, correct categorisation). Semantic sorting of bullets is where agents disagree with the judge. |
| pediatic-032 | pediatric glasses | Add a chart from the slide 13 table | Deterministic chart presence plus VLM "chart reflects table data". Agent must parse the table cells and build a native chart. |
| pediatic-035 | pediatric glasses | "Three Content" layout with a new unilateral-vs-bilateral column | Layout name exact match; two VLM nodes for three visible columns and the new column's content. The target layout may not exist in the deck's master. |
| application+layer+slide-021 | application layer | Replace the URL example and update the breakdown labels | VLM checks the new URL and that every component label (scheme, host, path) matches the new URL. Partial label updates fail the non-critical node. |

Why this set: all are "edit existing content" rather than "draw a new diagram", so a text-and-XML agent has a fair chance; they cover the four rubric families (layout, tables/charts, geometry, formatting) and nine decks.

## 5. Harness and pipeline validation

`scripts/` contains everything needed to run the CLI track here without
PowerPoint Online, Docker or an API key:

- `claude_judge.py`: drop-in `vlm_call` / `llm_call` that shell out to
  `claude -p` with only the `Read` tool allowed, so the judge can view the
  LibreOffice-rendered slide images. Every call is logged to
  `$CLAUDE_JUDGE_LOG` (prompt, image paths, response, model, cost).
- `run_claude_code_baseline.py`: thin wrapper over the repo's own
  `ppteval.run_benchmark` that installs the judge, forces
  `--conversion-mode libreoffice+poppler`, and with `--no-bypass` replaces
  Claude Code's `--dangerously-skip-permissions` by
  `--permission-mode acceptEdits --allowedTools ...`. The bypass flag was
  denied by this session's permission classifier; the narrower form ran
  unattended.
- `claude-code-default.yaml`: agent config with no model pin (CLI default,
  recorded from telemetry) and a 15-minute per-task cap.
- `make_smoke_deck.py` and `smoke_registry/`: the synthetic deck generator and
  synthetic task registry used below.

### Smoke test on a synthetic deck (NOT a benchmark result)

To prove the pipeline, a 4-slide deck was generated with python-pptx and a
synthetic task `SMOKE-001` ("change 'Lecture 3' to 'Lecture 1' in the title
and in the 'Lec 3.n' footers") was registered with a 4-leaf rubric in the
benchmark's own format: two deterministic python-pptx checks, one
`ppt_diff`-based extraneous-change check, and one `vlm_call` node comparing
the rendered title slide before and after.

| Stage | Outcome |
|---|---|
| Workspace seeding (`claude-workspace/` + Anthropic `pptx` skill, TASK.md, OUTPUT_INSTRUCTIONS.md) | OK |
| Claude Code run (`--permission-mode acceptEdits`, CLI default model `claude-sonnet-5-5`) | 4 turns, 3 Bash calls, 11.5 s, output file written |
| LibreOffice 24.2 + poppler rendering of original and output | 4 slides each, about 5 s per deck |
| Deterministic rubric leaves | 3 / 3 passed |
| VLM leaf, Claude-judged (`claude-sonnet-5-5`, 6.8 s) | PASS with a correct one-sentence rationale |
| Final rubric score | 1.00 (synthetic task; says nothing about PPT-Eval difficulty) |

Artefacts of this run (transcript, scored rubric, judge log) are kept out of
the repo; they are in the session's `/home/user/bench/results_smoke/`.

## 6. Reproduction

```bash
# 1. Benchmark checkout (outside this repo) and package
mkdir -p ~/bench && cd ~/bench
git clone --depth 1 https://github.com/microsoft/ppteval.git
git clone --depth 1 -b gh-pages https://github.com/microsoft/ppteval.git ppteval-site   # published numbers
cd ppteval && uv venv .venv -p 3.13 && uv pip install --python .venv/bin/python -e .

# 2. Anthropic pptx skill into the per-task workspace seed
mkdir -p claude-workspace/.claude/skills && cp -r /mnt/skills/public/pptx claude-workspace/.claude/skills/

# 3. Decks (BLOCKED here: archive.org denied). Skips PowerPoint Online normalisation.
# Names must match `file_path` in task_registry/tasks.json (URL-decoded basename,
# with the one doubled ".pptx.pptx" collapsed), e.g. "application+layer+slide.pptx".
.venv/bin/python - <<'PY'
import subprocess, urllib.parse, os
for u in open("data/files/PowerPoint/files.txt").read().split("\n"):
    if not u.strip(): continue
    name = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(u).path)).replace(".pptx.pptx", ".pptx")
    subprocess.run(["curl", "-fL", "--retry", "3", "-o", f"data/files/PowerPoint/{name}", u], check=True)
PY

# 4. Pipeline smoke test (synthetic deck, no benchmark data needed)
S=/path/to/this/dir/scripts
mkdir -p ~/bench/smoke_root && cp -r $S/smoke_registry/task_registry ~/bench/smoke_root/
.venv/bin/python $S/make_smoke_deck.py ~/bench/smoke_root
CLAUDE_JUDGE_LOG=~/bench/judge_smoke.jsonl .venv/bin/python $S/run_claude_code_baseline.py --no-bypass \
  --agent-config $S/claude-code-default.yaml --task-registry ~/bench/smoke_root/task_registry \
  --task-ids SMOKE-001 --results-dir ~/bench/results_smoke --timeout-minutes 15

# 5. The planned Hard-tier run (once decks are in data/files/PowerPoint/)
CLAUDE_JUDGE_LOG=~/bench/judge_hard.jsonl .venv/bin/python $S/run_claude_code_baseline.py --no-bypass \
  --agent-config $S/claude-code-default.yaml --results-dir ~/bench/results_hard --timeout-minutes 15 --concurrent 2 \
  --task-ids "3-009,4._Pre-Colonial_Filipino_Culture-020,Accounting Equation-008,Accounting Equation-012,Aircraft_surface-004,HSC Careers and Expo FINAL COM MOD-038,HSC Careers and Expo FINAL COM MOD-072,Jean-Nicolas-Louis Durand-008,Obesity-020,pediatic glasses when to prescribe1-032,pediatic glasses when to prescribe1-035,application+layer+slide-021"
# Per-task outputs: results_hard/<task_id>/{result.json,scored_rubric.json,cli_telemetry.json,workspace/output/<task_id>.pptx}
# Summary: results_hard/benchmark_summary.json (success = score 1.0; avg score = partial credit incl. extraneous-edit penalties)
```

Run the grader alone on existing outputs with `--verify-only --results-dir ...`.

## 7. Caveats

- No benchmark task executed, so there are no success rates, partial scores
  or observed failure modes. The risk notes in section 4 come from reading
  the rubric code.
- The judge is Claude (`claude-sonnet-5-5` via the CLI), not the paper's
  judge model. Label any VLM-scored node produced with this harness
  "Claude-judged"; the paper's meta-evaluation (Kendall tau-b 0.77 against
  humans) does not transfer.
- Rendering uses LibreOffice instead of PowerPoint Online or COM. SmartArt,
  some chart types and theme effects render differently, which affects VLM
  nodes on tasks such as Accounting Equation-015 and pediatic-019.
- Skipping PowerPoint Online normalisation can inflate "extraneous change"
  penalties for any agent that re-saves through python-pptx.
- The CLI default model answered as `claude-sonnet-5-5`; the published
  numbers are for GUI computer-use agents, and the repo's own CLI-track
  presets target Opus 4.5 / 4.7, so comparisons across tracks are indicative
  only.
- The agent ran with `acceptEdits` plus an explicit tool allow-list rather
  than the repo's bypass flag. Functionally equivalent for this workload
  (the smoke run never hit a permission prompt), but it is a deviation from
  the published configs.
