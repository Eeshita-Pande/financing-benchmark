# Slide / PowerPoint benchmark review and task hypotheses

Date: 2026-10-13. Purpose: pick the slide-type benchmarks we should review, run as baselines, and
learn from before building our own financing-deck tasks (see `task.md` for the Northstar Compute
exercise this repo already contains).

Scope note: arXiv was not reachable from the session that wrote this, so figures below come from
project pages, GitHub READMEs, leaderboards and search snippets. Verify numbers against the papers
before quoting them externally.

---

## 1. Benchmarks to review and run

### Tier 1: run these as baselines (PPTX-native, agentic, code available, not saturated)

| Benchmark | What it tests | Size | Scoring | Best reported result | Code |
|---|---|---|---|---|---|
| **PPTArena** (arXiv 2512.03042, ECCV 2026) | Editing existing decks: text, charts, animations, master styles; compound, cross-slide and layout-sensitive edits | 100 decks, 2,125 slides, 1,300+ human-curated edits | Two VLM judges: instruction-following from structural diffs, visual quality from renders | Live leaderboard: Claude CUA 48.4, Codex (GPT-5.5) 43.6, Claude Code (Opus 4.8) 42.8; the 25-case "hard" subset scores far lower | github.com/michaelofengenden/PPTArena, leaderboard at ppt-arena.onrender.com |
| **PPT-Eval** (arXiv 2606.31154, ICML 2026, Microsoft + Neubig) | Computer-use agents driving PowerPoint through a browser GUI; creation and editing | 120 tasks across 12 files, tiered by difficulty | Rubrics with partial credit and penalties for extraneous edits (Kendall tau 0.77 vs humans) | Claude 4.5 Opus 45% success, 0.57 partial; humans 80% success, 0.90 partial | microsoft.github.io/ppteval |
| **DocOps** (arXiv 2607.19865) | End-to-end Office document operations across XLSX, DOCX, PPTX, PDF with deterministic validators on the native file | 210 tasks: L1 atomic (50), L2 compositional (40), L3 single-document workflow (60), L4 cross-document workflow (60) | Deterministic per-task validator reading the output file | Strongest configs fail about a third of tasks; near-collapse on L4 cross-file workflows | github.com/icip-cas/DocOps |
| **BankerToolBench** (arXiv 2604.11304, Handshake AI) | End-to-end junior-banker workflows producing Excel + PowerPoint + Word deliverables (models, pitch decks, memos) | 100 tasks, ~5 h human time each, ~150 weighted pass/fail rubric criteria each | Agentic verifier ("Gandalf"); dimensions: Technical Correctness, Client Readiness, Internal Consistency, Risk & Compliance | GPT-5.4 fails nearly half of criteria; bankers rate 0% of outputs client-ready | github.com/Handshake-AI-Research/bankertoolbench (Harbor task suite, Docker) |
| **PresentBench** (arXiv 2603.07244) | Rubric-based slide generation from a brief across Academia, Education, Economics, Talk, Advertising | 238 instances, ~54 binary checklist items each | Binary checklist, five dimensions incl. Content Fidelity, Visual Design & Layout | NotebookLM 62.5, Manus 1.6 57.8, PPTAgent v2 50.2; Visual Design is the weakest dimension (Gamma 22.6) | presentbench.github.io |

Why these five: together they cover the three regimes we care about (file-level editing, GUI
editing, and multi-file professional workflows) and all of them still have a large gap to human
performance.

### Tier 2: review for evaluation methodology and task ideas

- **SlidesGen-Bench** (arXiv 2601.09487, EMNLP 2026, MIT licence). Three measurable axes: content
  fidelity via a VLM "QuizBank" open-book exam on the rendered deck, computational aesthetics
  (harmony, contrast, clutter), and a six-level editability scale (PEI) parsed from the file.
  Spearman 0.71 against human rankings. Useful as a reusable scorer. github.com/YunqiaoYang/SlidesGen-Bench
- **UniPPTBench** (arXiv 2605.17356). Four input settings: vague prompt, long document, multimodal
  document, multi-source. Reports recurring failures in content grounding and cross-source synthesis.
- **X+Slides** (arXiv 2606.19256). Audience-conditioned generation: same source, different audience,
  scored with 8,133 source-grounded probes weighted per audience. Best systems recover a large but
  incomplete share of audience-essential content.
- **DECKBench** (arXiv 2602.13318, KDD 2026). Paper-to-slides plus multi-turn editing with a
  simulated user and three personas. Release at github.com/morgan-heisler/DeckBench.
- **DeckEdit-Bench** (from EditPPT, arXiv 2608.20381). 28 human-authored decks, 582 slides, 183
  edit prompts; scores instruction following and object preservation separately. Good model for
  "do not break anything else" metrics.
- **TSBench** (from Talk to Your Slides, arXiv 2505.11604, ACL 2026 Findings). 379 human-verified
  edit instructions with a Hard subset; compares file-level agents to GUI agents on cost and fidelity.
- **Office Comprehension Benchmark** (arXiv 2607.01245, Microsoft). Read-only comprehension of
  native Office files. PowerPoint file-fidelity track is near-saturated (Claude Opus 4.7 86.6%,
  GPT-5.5 85.9%), so comprehension alone is not a frontier task.

### Tier 3: image-to-editable reconstruction (adjacent, useful for chart tasks)

- **PPTBench** (arXiv 2609.29718). 500 scientific flow diagrams to rebuild as editable slides; 36
  model-harness-effort configs; best 77.3/100, median 24.4. Large harness and effort effects.
- **ReFigBench** (arXiv 2609.18844). 1,000 arXiv overview figures to editable PPTX; isolates harness
  effect by running the same model in Claude Code and Codex. Best 77.4/100.
- **Slide2Code / SlideCoder** (arXiv 2506.07964). Slide image to python-pptx code, three difficulty tiers.

### Older or general benchmarks (context and history, not primary baselines)

- **PPTC / PPTC-R** (arXiv 2311.01767, ACL 2024 Findings). GPT-4 reached 75% turn-level accuracy
  but only ~6% session-level accuracy because errors accumulate across turns. The session-level
  framing is still the best evidence that multi-turn deck work is hard.
- **SlidesBench / AutoPresent** (arXiv 2501.00912, CVPR 2025). 585 test examples, text to python-pptx
  code; largely saturated on execution rate.
- **OfficeBench** and **OdysseyBench** (arXiv 2407.19056, 2508.09124). Multi-app office workflows;
  OfficeBench excludes PowerPoint.
- **OSWorld-Verified**. General GUI agent benchmark, now at 85%+ for top agents, with an audit
  finding many hard-task checkers are weak. OSWorld 2.0 (108 long-horizon multi-app tasks) sits
  around 20% for the best agent. No published Impress-only breakdown found.
- **GDPval** (OpenAI). Occupational deliverables including PPTX; the paper notes Claude did better on
  PDF, Excel and PowerPoint deliverables than on pure text. Useful as a win-rate grading pattern.
- **APEX-Agents 1.1** (Mercor). Investment banking, consulting and law tasks in data-rich
  environments; top public score around 82% on the 1.1 revision, so the easy portion is saturating.
- **SlideAudit** (arXiv 2508.03630) and **Paper2Poster** (NeurIPS 2025 D&B). Design-flaw taxonomy
  and the PaperQuiz content test, both reusable as graders.

---

## 2. What is saturated and what is not

Saturated or close to it (do not build tasks here):
- Reading and answering questions about a PPTX (OCB ~87%).
- Single atomic edits on one slide (DocOps L1, PPTArena easy, TSBench non-hard).
- Generating a plain text-to-slides deck that executes (SlidesBench execution ~90%).
- Basic GUI navigation (OSWorld-Verified 85%+).

Still open (evidence in brackets):
1. **Compound, cross-slide and layout-sensitive edits** on real decks (PPTArena hard subset).
2. **Driving the actual PowerPoint GUI** (PPT-Eval: 45% vs 80% human).
3. **Long, cross-file workflows** where state must be tracked across xlsx, docx and pptx
   (DocOps L4 collapse; BankerToolBench cross-artifact consistency failures).
4. **Client readiness**: outputs that are structurally complete but wrong in detail
   (BTB 0% client-ready; PresentBench "Completeness higher than Correctness").
5. **Visual design and layout quality** measured by strict rubrics (PresentBench visual dimension
   is the weakest for almost every system).
6. **Audience conditioning**: choosing what to include for a given reader (X+Slides).
7. **Multi-turn error accumulation** (PPTC session 6% vs turn 75%).
8. **Non-destructive editing**: preserving master layouts, animations and untouched objects
   (DeckEdit-Bench object preservation; DocOps "destructive editing of structural metadata").
9. **Native charts with correct data** rather than images (PresentBench checks bar heights and
   pie angles; SlidesGen-Bench editability levels).

---

## 3. Task hypotheses for a financing-deck benchmark

Each hypothesis names the gap it targets, the input we already have or can build from the Northstar
Compute materials, and how it can be verified. Verification should be deterministic where possible
(parse the PPTX XML and compare with the workbook) and rubric-based only where judgement is needed.

**H1. Model-to-deck numeric fidelity.** Given `model.xlsx` (or a reference solution), build the
investment-committee deck. Every number on every slide must match the workbook to stated rounding,
with units and periods labelled. Targets gaps 3 and 4. Verify by extracting all numerals from the
PPTX (text, tables, chart series) and reconciling against named workbook outputs; score the
proportion matched and flag fabricated figures.

**H2. Assumption change propagation.** Start from a correct deck and workbook, then revise one
committee assumption (price, delay month, support cap). The agent must update the workbook and
re-issue the deck so that all dependent slides, charts and footnotes change consistently. Targets
gaps 3, 7 and 8. Verify by diffing against the recomputed reference and checking that unrelated
slides are byte-identical in content.

**H3. Four-case comparison slides with native charts.** Produce case-comparison slides (DSCR path,
cash path, funding shortfall, sponsor IRR) as editable native chart objects with correct series,
axes and categories, not pasted images. Targets gap 9. Verify by parsing chart XML: series values
equal the workbook, chart type appropriate, no image placeholders.

**H4. Covenant exposition with the operating/post-cure distinction.** Slides must show the operating
DSCR and the ratio after permitted cure separately, mark untested commissioning months, and show
unresolved breaches as unresolved rather than as a funded plan. Targets gap 4 (domain correctness
inside a presentation). Verify with a rubric derived directly from `funding.md` sections 3 and 4.

**H5. Edit an existing bank-template deck under amendments.** Provide a 30-slide template deck and
the contract amendment from `contracts.md`. The agent must apply the amendment everywhere it bites
(pricing, renewal clause, collections slide, appendix table) while preserving the slide master,
theme, footers and animations. Targets gaps 1 and 8. Verify instruction coverage with a rubric and
preservation with an XML diff against untouched slides.

**H6. Audience re-cut with disclosure constraints.** From the same materials produce three decks:
lender (no sponsor return, covenant focus), sponsor (return and support usage), committee (both).
Items that must appear and must not appear are enumerated per audience. Targets gap 6. Verify by
presence/absence checks on required and prohibited facts.

**H7. Cross-artifact consistency: deck plus memo plus model.** The full deliverable is
`model.xlsx`, `recommendation.md` and `deck.pptx`. Score agreement of key figures and conclusions
across all three. Targets gap 3 and BTB's leading failure mode. Verify by extracting the same named
metrics from each artifact and comparing.

**H8. Red-flag review of a flawed deck.** Give a deck with planted errors (stale number, wrong
period label, chart series off by one case, DSCR shown post-cure but labelled operating, sum that
does not foot). The agent must find and list them with slide references, and optionally fix them.
Targets gap 4 from the reviewer side. Verify against the planted-error list with precision and
recall.

**H9. Multi-turn committee session.** A simulated committee member asks for successive changes over
8 to 12 turns (add sensitivity, move slide, change case naming, re-base chart). Score the final
deck only, as PPTC session-level does, plus a per-turn preservation check. Targets gap 7.

**H10. Layout quality under strict rubric.** Apply a PresentBench-style binary checklist to our
generated decks: no text overflow, consistent fonts and colours, readable chart labels, aligned
tables, balanced text and visuals. Targets gap 5. Verify by rendering through LibreOffice and
running overflow and overlap detection, plus a VLM judge for the subjective items.

**H11. Same task, two harnesses: file-level versus GUI.** Run H1 or H5 both through python-pptx
style file editing and through a PowerPoint GUI (PPT-Eval environment). Measure the harness gap and
cost. Targets gap 2 and the harness effects seen in PPTBench and ReFigBench.

**H12. Provenance and footnoting.** Every figure or claim on a slide must cite its source section
(`contracts.md` clause, `funding.md` section, workbook sheet). Targets gap 4. Verify by checking
footnote presence and that the cited location actually contains the fact.

**H13. Date and return conventions rendered correctly.** Annualised return on an actual/365 basis
from specified cash-flow dates, month-end timing, and rounding must be consistent across the
summary slide, the appendix and the workbook. Small but frequently wrong; verify numerically.

Suggested priority for a first build: H1, H3, H5, H7, H8. They reuse the existing Northstar
materials, have deterministic graders, and each targets a gap with published evidence that frontier
agents fail today.

---

## 4. Running plan

1. **PPTArena**: clone the repo, run the hard subset with Claude Code, Codex and a GUI agent to
   reproduce the leaderboard ordering. Reuse its two-judge design (structural diff plus render).
2. **PPT-Eval**: bring up the sandboxed browser PowerPoint environment and run the 120 tasks with
   our preferred computer-use agent; keep its rubric format for partial credit.
3. **DocOps**: run L3 and L4 only; study its deterministic validators as the pattern for H1 to H3.
4. **BankerToolBench**: run the pitch-deck tasks through the Harbor suite (needs Docker and
   20 to 30 GB disk); copy its rubric dimensions (Technical Correctness, Client Readiness,
   Internal Consistency, Risk & Compliance) for our rubrics.
5. **PresentBench and SlidesGen-Bench**: do not re-run in full; adopt the checklist style and the
   QuizBank and editability scorers for H10.

---

## Sources

- PPTArena: https://arxiv.org/abs/2512.03042 , https://github.com/michaelofengenden/PPTArena , https://ppt-arena.onrender.com/evaluation
- PPT-Eval: https://arxiv.org/abs/2606.31154 , https://microsoft.github.io/ppteval/
- DocOps: https://arxiv.org/abs/2607.19865 , https://github.com/icip-cas/DocOps
- BankerToolBench: https://arxiv.org/abs/2604.11304 , https://github.com/Handshake-AI-Research/bankertoolbench
- PresentBench: https://arxiv.org/abs/2603.07244 , https://presentbench.github.io/
- SlidesGen-Bench: https://arxiv.org/abs/2601.09487 , https://github.com/YunqiaoYang/SlidesGen-Bench
- UniPPTBench: https://arxiv.org/abs/2605.17356
- X+Slides: https://arxiv.org/abs/2606.19256
- DECKBench: https://arxiv.org/abs/2602.13318 , https://zenodo.org/records/20318469
- EditPPT / DeckEdit-Bench: https://arxiv.org/abs/2608.20381
- Talk to Your Slides / TSBench: https://arxiv.org/abs/2505.11604
- Office Comprehension Benchmark: https://arxiv.org/abs/2607.01245 , https://huggingface.co/datasets/microsoft/OfficeComprehensionBenchmark
- PPTBench: https://arxiv.org/abs/2609.29718
- ReFigBench: https://arxiv.org/abs/2609.18844
- SlideCoder / Slide2Code: https://arxiv.org/abs/2506.07964
- PPTC: https://arxiv.org/abs/2311.01767
- AutoPresent / SlidesBench: https://arxiv.org/abs/2501.00912
- OfficeBench: https://arxiv.org/abs/2407.19056 ; OdysseyBench: https://arxiv.org/abs/2508.09124
- OSWorld-Verified leaderboard: https://benchlm.ai/benchmarks/osworld-verified
- GDPval: https://www.researchgate.net/publication/400195012_GDPVAL_Evaluating_AI_Model_Performance_on_Real-World_Economically_Valuable_Tasks
- APEX-Agents 1.1: https://benchlm.ai/benchmarks/mercorapexagents11
- SlideAudit: https://arxiv.org/abs/2508.03630 ; Paper2Poster: https://arxiv.org/abs/2505.21497
