# PPTArena baseline: Claude Code on the failing tasks

Date: 2026-10-13. Benchmark: [PPTArena](https://github.com/michaelofengenden/PPTArena) (agentic PowerPoint editing, 100 cases, 25-case hard subset), cloned at depth 1 on the run date.

**Read the caveats first.**

- **Agent under test:** Claude Code, run as in-session subagents (the general-purpose agent type) of the orchestrating Claude Code cloud session, not as the `claude -p` CLI process that the leaderboard harness uses. The subagents therefore ran on that session's configured model, not on the `claude-opus-4-8` model named in the benchmark's `agents.json` and not on the CLI's default model. The exact model identifier is recorded in the orchestrating session's metadata and in the run report sent to the orchestrator; it is deliberately not written into this repository.
- **Judge:** a fresh Claude Code subagent of the same session, so the judge is the **same model family (and the same configured model) as the agent under test**. Every score below is **Claude-judged, not the official judge**. Self-family judging can be lenient toward the agent's own conventions. - **Comparison baseline:** the recorded leaderboard rows were themselves judged by Kimi K2.6 (median of 3), not by GPT-5 or Gemini, which the repo's own scripts treat as alternatives. Two different judges with different harshness are being compared, so treat the comparison as directional only.

## 1. Summary

| Metric (11 failing cases) | This run (Claude-judged) | Recorded agents (Kimi-judged) |
|---|---|---|
| Mean instruction-following (0-5) | 3.36 | 0.64 to 2.27 per agent (mean over 8 agents: 1.29) |
| Mean visual quality (0-5) | 2.82 | 0.18 to 2.73 per agent |
| Mean combined (IF+VQ)/2 | 3.09 | 1.26 mean of agents; 2.55 taking the best agent per case |
| Combined score vs best recorded agent on same case | 7 higher, 3 equal, 1 lower | |
| Runs that produced a valid, rendering deck | 11 / 11 | |
| Wall time per case | 117 s to 253 s (median 169 s) | leaderboard caps at 2400 s |

Every run produced a deck that opens with python-pptx 1.0.2 and converts with LibreOffice, and every run changed the deck. No run timed out. The highest-scoring recorded agent over these 11 cases is Codex GPT-5.5 (mean combined 2.27), then Baidu DuMate (2.18) and Claude Code Opus 4.8 (1.68).

**Top 3 failure patterns in this run** (details in section 5):

1. **Layout reflow after a content edit is not re-checked.** Lengthening a chart series name (Case 7) overflowed a manually sized legend box; the agent saw the clipped legend in its own render and blamed the renderer instead of resizing the box. Narrowing a text column (Case 54) caused extra wrapping. Rebuilt bibliography text (Case 83) lost italics and the slide-number placeholder because the agent typed new text instead of copying runs.
2. **Under-specified instructions are resolved differently from the reference.** "As well as the second one" (Case 98), what a "unique title" is for a screen reader (Case 67), whether year-less dates should get a year (Case 50), what to call a slide with no title (Case 54). The recorded agents fail the same cases, which suggests part of the hard subset measures agreement with one annotator's reading rather than editing competence.
3. **Style conventions already in the deck are not reused.** New charts (Cases 30 and 93) carried the right data but not the deck's existing chart styling (axis style, significance markers, legend placement), and new slides used layout defaults rather than copying neighbouring slides' font sizes.

Perception and tooling were rarely the blocker: in every case the agent inspected the OOXML or rendered PNGs and used python-pptx or lxml successfully, including cross-slide picture moves, layout rebinding at the rels level and native chart creation. The remaining gap to a perfect score is mostly judgement and verification discipline, not capability.

## 2. Inventory: where frontier models fail

Sources inside the PPTArena clone: `src/evaluation_pairs_refined.json` (100 cases: prompt, hidden style target, original and ground-truth decks, edit type), `agent_bench/subset25.json` (the 25-case hard subset), and `agent_bench/results/*_judge_results.csv` (per-case instruction-following and visual-quality scores, 0-5). The `*_judge_results.csv` files carry judge model `kimi-k2.6 (median of 3)`; the `*_qwen_judge_results.csv` files carry `qwen/qwen3.7-plus (median of 3)`. The two older JSON files (`evaluation_results_bulk.json`, Gemini 3.1 Pro code-generation pipeline on 100 cases; `claude_evaluation_results.json`, 25 hand-made Claude edits) were read but not used for the failing-set definition because they are not CLI agents. Three `cua_*` and two `pptpilot_*` result files cover only the 25-case subset and were also excluded from the mean.

Eight recorded agents cover all 100 cases with the Kimi judge: Codex GPT-5.5, Claude Code Opus 4.8, Gemini CLI 3.5 Flash, OpenCode with DeepSeek V4 / GLM-5.2 / Kimi K2.7 / MiniMax-M3, and the Baidu DuMate pptx skill. For each case the per-agent combined score is (IF+VQ)/2, and the case score is the mean over the eight agents. The distribution is low across the board: median case score 2.00, bottom quartile 1.39.

**Failing set definition:** the 25-case hard subset, plus every case whose mean combined score is at or below the bottom-quartile threshold of 1.39. That is 46 cases. Grouped by the benchmark's `edit_type`:

| Edit type | Failing cases (mean of per-agent (IF+VQ)/2 over the 8 recorded CLI/skill agents; * = in the 25-case hard subset) |
|---|---|
| Text & Typography | Case 97* (0.31), Case 19 (0.75), Case 4 (1.06), Case 85 (1.06), Case 1 (1.31), Case 34* (1.31), Case 35* (1.50), Case 89* (1.56), Case 40* (1.69), Case 12* (1.94), Case 21* (2.19) |
| Theme & Background | Case 38 (0.62), Case 80 (0.94), Case 45 (1.19), Case 54* (1.25), Case 76 (1.31), Case 77 (1.31) |
| Slide/Section Management & Footers | Case 83 (1.12), Case 43 (1.25), Case 39 (1.38), Case 28* (2.50), Case 87* (3.38) |
| Charts | Case 93 (1.12), Case 7* (1.56), Case 6* (1.62), Case 30* (2.12), Case 47* (4.94) |
| Images & Pictures | Case 69 (0.75), Case 92* (1.56), Case 44* (1.75), Case 27* (3.62) |
| SmartArt & Diagrams | Case 72 (0.75), Case 98 (1.31), Case 46* (1.50) |
| Alignment, Distribution & Z-order | Case 88 (0.75), Case 16* (2.31), Case 42* (2.75) |
| Tables | Case 50* (0.88), Case 53* (1.94) |
| Slide Layout & Placeholders | Case 94 (1.19), Case 90 (1.38) |
| Accessibility & Semantics | Case 96 (1.31), Case 67* (1.44) |
| Shapes & Drawing | Case 57* (1.94), Case 17* (2.62) |
| Template & Master-Level Edits | Case 95 (1.12) |

The full 46-row table with per-agent IF/VQ is in the appendix at the end of this file. The whole table for all 100 cases is reproducible from the clone with the commands in section 6.

Three observations from the inventory:

- Charts: three of the five chart cases are in the hard subset and all score at or below 2.1 except the trivial Case 47 (line to bar), which every agent gets right. Case 93 (image to native chart plus five other edits) is the hardest chart case because agents drop sub-edits.
- Cross-slide and structural edits (Cases 69, 83, 98, 28, 87) score low mainly on visual quality: agents change the right slide but disturb layout, or do not move objects between slides at all.
- Master, theme and layout edits (Cases 38, 80, 54, 95, 94, 67) are the weakest group after text-heavy translation. Recorded agents typically edit shapes on individual slides instead of rebinding layouts or touching the master.

## 3. What was run

Eleven cases were chosen from the failing set to cover charts, cross-slide, layout-sensitive, master/style and table edits, which matter most for the financing-deck benchmark:

| Case | Why chosen |
|---|---|
| 7 Update Quarter Two Data (B) | hard subset, charts with embedded workbooks, cross-slide text replace, font edits |
| 30 Convert Text Data to a Line Chart | hard subset, chart creation from text, custom legend |
| 93 Multi-Edit Cascade | lowest-scoring chart case, six chained edits including image-to-chart |
| 98 Cross-Slide Conditional Formatting | table on one slide drives shape fills on another |
| 69 Cross-Slide Image-Caption Correlation | needs image perception plus cross-slide moves |
| 94 Slide Size 4:3 to 16:9 | master, layouts and every slide must change together |
| 95 Master and Layout Rebind | layout rebinding at the relationship level |
| 54 Match Slide Deck Theme | hard subset, propagate one slide's layout to seven others |
| 50 Normalize Date Format | hard subset, 15-slide table-heavy legal deck, many date formats |
| 83 Bibliography Slide from Footers | cross-slide extraction and new slide |
| 67 WCAG Accessibility and Master Cleanup | hard subset, master-level font cleanup, lowest IF for every recorded agent |

Procedure per case (mirrors `agent_bench/run_agents.py`): copy the original deck to an isolated workdir as `deck.pptx`, write `INSTRUCTION.md` with the case prompt, run the agent with the same task prompt text the leaderboard uses (edit in place, keep the filename, preserve everything else, verify the file opens), with a stated budget of about 15 minutes. The agent was told it may not read the benchmark clone, so it could not see the ground truth. After the run: hash comparison with the original, zip and python-pptx validity, LibreOffice render to PDF then PNG, slide/chart/table counts, and a shape-level structural diff against the original and the ground truth.

**Deviation from the leaderboard harness.** The orchestrator asked for `claude -p ... --dangerously-skip-permissions` (the exact invocation in `agent_bench/agents.json`). Both that flag and a narrower `--allowedTools` allowlist were refused by this session's permission classifier as creating an unsafe nested agent. The agent under test is therefore a Claude Code **subagent** of this session (the general-purpose agent type with Bash, Read, Write, Edit, Glob and Grep), given the same prompt. Same harness family and tools, but: it runs on this session's model rather than the Opus 4.8 model named in `agents.json`; it inherits this session's permission mode; and its wall time includes subagent start-up. Wall time was measured from a `.started` stamp written before launch to a `.finished` stamp the agent wrote as its last action.

## 4. Scores

All "this run" scores are **Claude-judged**: a fresh Claude Code subagent per case received the case instruction, the hidden style target, the instruction-following and visual-quality rubric text copied verbatim from `src/llm/judge.py` (arena mode), a focused ground-truth-vs-prediction structural diff produced by `scripts/collect.py`, and the LibreOffice-rendered PNGs of every ground-truth and prediction slide, which it viewed with the Read tool. It wrote one JSON with both scores and one-sentence reasons. Differences from the official judge: the official pipeline uses its own `ppt_processor.diff_pptx_json` (ours is a python-pptx shape summary diff that also captures fills, chart series and table cells), batches images with SSIM/pHash pre-filtering for large decks (ours shows every slide), and takes a median of three samples (ours is a single sample). Recorded columns are the Kimi-K2.6-judged leaderboard rows for the same cases.

| Case | Type | Subset | Status | Wall (s) | **This run IF/VQ** (Claude-judged) | Codex GPT-5.5 | Claude Code Opus 4.8 | Gemini CLI 3.5F | OC DeepSeek V4 | OC GLM-5.2 | OC Kimi K2.7 | OC MiniMax-M3 | Baidu DuMate | Recorded mean | Recorded best |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Case 7: Update Quarter Two Data (B) | Charts | yes | ok | 253 | **3/2** | 2/2 | 1/2 | 1/1 | 1/2 | 1/2 | 1/2 | 1/1 | 1/4 | 1.56 | 2.5 |
| Case 30: Convert Text Data to a Line Chart | Charts | yes | ok | 177 | **4/3** | 4/0 | 3/0 | 4/1 | 3/0 | 4/2 | 4/0 | 3/0 | 3/3 | 2.12 | 3.0 |
| Case 93: Multi-Edit Cascade (Copernicus Clima | Charts | no | ok | 169 | **4/3** | 3/3 | 2/2 | 2/2 | 0/0 | 0/0 | 0/0 | 0/0 | 1/3 | 1.12 | 3.0 |
| Case 98: Cross-Slide Conditional Formatting ( | SmartArt & Diagrams | no | ok | 117 | **3/2** | 2/2 | 2/2 | 3/2 | 0/0 | 0/0 | 2/2 | 0/0 | 2/2 | 1.31 | 2.5 |
| Case 69: Cross-Slide Image–Caption Correlatio | Images & Pictures | no | ok | 176 | **3/3** | 2/3 | 1/1 | 1/1 | 0/0 | 0/0 | 0/0 | 0/0 | 1/2 | 0.75 | 2.5 |
| Case 94: Slide Size Conversion 4:3 → 16:9 | Slide Layout & Placeholders | no | ok | 136 | **4/3** | 2/4 | 1/1 | 1/1 | 0/0 | 0/0 | 1/3 | 0/0 | 1/4 | 1.19 | 3.0 |
| Case 95: Master & Layout Rebind | Template & Master-Level Edits | no | ok | 122 | **5/3** | 3/1 | 3/2 | 3/1 | 0/0 | 0/0 | 0/0 | 0/0 | 3/2 | 1.12 | 2.5 |
| Case 54: Match Slide Deck Theme | Theme & Background | yes | ok | 208 | **3/3** | 2/2 | 2/1 | 2/1 | 2/1 | 2/1 | 0/0 | 0/0 | 2/2 | 1.25 | 2.0 |
| Case 50: Normalize Date Format | Tables | yes | ok | 151 | **3/4** | 1/1 | 1/1 | 1/1 | 1/0 | 1/1 | 0/0 | 1/1 | 1/2 | 0.88 | 1.5 |
| Case 83: Bibliography Slide from Footers | Slide/Section Management & Footers | no | ok | 158 | **3/3** | 3/3 | 2/2 | 2/0 | 0/0 | 0/0 | 0/0 | 2/0 | 2/2 | 1.12 | 3.0 |
| Case 67: WCAG Accessibility & Master Cleanup | Accessibility & Semantics | yes | ok | 236 | **2/2** | 1/4 | 1/4 | 1/2 | 1/2 | 0/2 | 0/0 | 0/0 | 1/4 | 1.44 | 2.5 |

Deterministic checks (all 11 cases): file changed, valid zip with `[Content_Types].xml`, python-pptx opens, LibreOffice renders every slide. Slide counts matched the ground truth in all cases (Case 93 and Case 83 correctly gained one slide). Chart counts matched the ground truth in Cases 7, 30, 93 and 94. Case 94's slide size changed to a 16:9 ratio (13.33 x 7.5 in; the ground truth used 10 x 5.63 in).

**Judge reliability check.** On Case 54 the first judge pass penalised "animations stripped from every slide". Inspection of the original shows it has no animations; only the ground truth gained `<p:timing>` nodes, so the diff line was a ground-truth artefact. A second pass with that fact added to the prompt is recorded in `results.json` under `claude_judge_rerun_corrected_diff_note` (re-run: IF 4 / VQ 3, versus 3 / 3 on the first pass; the IF reason no longer mentions animations). The table above keeps the first-pass score. This is one of eleven cases, so similar artefacts elsewhere cannot be ruled out.

## 5. Per-case analysis

### Case 7: Update Quarter Two Data (B)

*Charts; hard subset; wall 253 s; Claude-judged IF 3 / VQ 2; recorded agents mean 1.56, best 2.5.*

**Instruction.** Please replace all instances of 'Q2' with 'Second Quarter' throughout the presentation. Also, on slide 9, change the title font size to 32pt. Finally, on slides 6, 7, and 9, please un-bold the text below the charts.

**Analysis.** Charts / cross-slide text replace. All three requested edits were applied, including inside chart caches and the embedded workbook, which is where most recorded agents stopped short (leaderboard IF 1-2). Two misses: a literal find-and-replace produced 'Second Quarter (Second Quarter) NOI' and mid-sentence capitalisation, and the agent un-bolded the wrong text under the slide-7 charts (the YTD callouts instead of the 'Q1 & Q2 YOY' label). The visible regression is a layout-reflow miss: lengthening the series name made the bar-chart legends overflow their manual legend box, so LibreOffice drops the 'Q1 YOY Var' entry on slides 7-8; the ground truth widened the legend box. Series data are intact (verified via python-pptx), so this is a perception/verification failure, not a tooling one: the agent saw the clipped legend in its own render and attributed it to LibreOffice instead of fixing the legend layout.

**Judge reasons (Claude-judged).** IF: Q2 replacements, the 32pt slide-9 title, and the un-bolding of the slide 6/9 x-axis label boxes match ground truth, but on slide 7 the prediction left TextBox 14 ('Q1 & Second Quarter YOY Activity Variance') bold (bold_runs: 1) while ground truth un-bolded it, and instead un-bolded the '-60% YTD'/'-56% YTD' labels that ground truth kept bold; it also used 'Second Quarter' mid-sentence on slides 6 and 9 where ground truth used contextual lowercase 'second quarter'. VQ: Slides 1-6 and 9-12 render essentially identically to ground truth, but on slides 7 and 8 the prediction's bar-chart legends lost the 'Q1 YOY Var' entry (only 'Second Quarter YOY Var' remains) in all four charts, a clear unintended change to non-requested chart content, and the slide-7 YTD callout labels were un-bolded where ground truth kept them bold.

### Case 30: Convert Text Data to a Line Chart

*Charts; hard subset; wall 177 s; Claude-judged IF 4 / VQ 3; recorded agents mean 2.12, best 3.0.*

**Instruction.** On slide 8, convert the text data showing uninsured rates into a line chart with markers. Also, create a custom legend for the chart on the right.

**Analysis.** Charts: text-to-chart conversion. The agent built a native LINE_MARKERS chart from the text box with exactly the right categories and series values, disabled the built-in legend and drew a custom legend from shapes, which is what the ground truth does. Recorded agents all reached IF 3-4 on this case but VQ 0-2; the Claude-judged VQ of 3 reflects styling drift (smaller chart, 0-20% axis with gridlines, missing '*' significance markers that the ground truth carried over from the text). Failure mode: the agent reproduced the data but not the deck's existing chart style conventions (slides 1-7 already contain styled KFF charts it could have copied).

**Judge reasons (Claude-judged).** IF: Prediction removed the original uninsured-rate text box on slide 8 and replaced it with a LINE_MARKERS chart whose categories (2013-2017) and three series (NHOPI, Asian, White) exactly match the original text values, hid the built-in legend (has_legend false) and added a 'Custom Legend' group to the right of the chart as the ground truth does, with all other slides untouched; only tiny divergences remain (an extra 'Uninsured rate (%)' legend title and a smaller chart footprint than the ground truth's full-width chart). VQ: Slides 1-7 and 9 render identically to ground truth, and slide 8 shows a clean, non-overlapping line chart with markers and a right-side custom legend, but it visibly differs from the ground truth's styling (smaller chart with a 0-20% vertical axis and gridlines, missing the '*' significance markers on data labels, and slightly crowded 18%/16% labels at 2013).

### Case 93: Multi-Edit Cascade (Copernicus Climate Highlights)

*Charts; not in hard subset; wall 169 s; Claude-judged IF 4 / VQ 3; recorded agents mean 1.12, best 3.0.*

**Instruction.** Please apply a consistent, professional theme to this presentation. Change all slide titles to a dark blue and all body text to a dark gray. On slide 4, replace the static image of the bar chart with an actual, editable column chart. On slide 5, rearrange the images and their captions for a better flow. Also, add a progress bar at the bottom of every slide. Finally, add a new 'Bibliography' slide at the very end with the source URL.

**Analysis.** Charts + multi-edit cascade. Six sub-edits were all executed (title/body colours, image-to-native-chart on slide 4, slide-5 re-layout, progress bar on every slide, new bibliography slide with URL). This is the case where recorded agents scored lowest on a chart task (mean 1.1, best 3.0) because they dropped sub-edits. Remaining gaps are judgement calls, not misses: chart values were inferred from slide text because the source was a bitmap (the ground truth used the same three bars), the chart was styled dark blue without a legend, and the bibliography body was left at the layout's default size so it runs close to the progress bar. Visual drift vs ground truth (white vs light-blue background, blue vs orange progress bar) is largely ground-truth taste.

**Judge reasons (Claude-judged).** IF: Prediction delivers every requested change matching the ground truth's outcome (dark-blue titles, dark-gray body, native COLUMN_CLUSTERED chart with the same categories/values replacing the image on slide 4, slide-5 images and captions rearranged with clear pairing, proportional progress bar 1/7..7/7 on every slide, a 7th 'Bibliography' slide with the climate.copernicus.eu URL, citation markers [1]-[6] preserved), with only small differences such as no chart legend, captions reset to 11pt, and bibliography body left at the large default size. VQ: All slides are clean, legible and overlap-free like the ground truth, but there are noticeable differences: the prediction keeps a white background where the ground truth uses light blue, uses a dark-blue instead of orange progress bar, and the Bibliography slide's body text is rendered at a much larger size than the GT's 16pt list so it runs down to the progress bar.

### Case 98: Cross-Slide Conditional Formatting (Status → Timeline)

*SmartArt & Diagrams; not in hard subset; wall 117 s; Claude-judged IF 3 / VQ 2; recorded agents mean 1.31, best 2.5.*

**Instruction.** Using the status table on slide 2, update the project timeline on slide 3. For any project marked 'At Risk', change its corresponding shape's fill color to red. Aswell as the second one.

**Analysis.** Cross-slide conditional formatting. The agent read the status table on slide 2 and recoloured the matching timeline shape on slide 3 correctly. The instruction's trailing clause 'Aswell as the second one' is ambiguous: the agent turned the second shape red too, while the ground truth coloured it green (theme accent 6) for an 'On Track' project. Recorded agents hit the same wall (IF 2-3 for every agent). This is an instruction-ambiguity failure rather than perception or tooling; a human would probably have asked.

**Judge reasons (Claude-judged).** IF: The prediction correctly turned the 'Mars Sample Return' shape (Shape 1) red and left the 'U.S. Renewable Energy Growth' shape and slides 1-2 intact, but it filled the second shape 'Kaheawa Wind Farm' (Shape 3) with SOLID:FF0000 red instead of the green (ACCENT_6) the ground truth uses for an 'On Track' project, so one of the two requested changes is applied with the wrong color. VQ: Slides 1 and 2 render identically to the ground truth and text stays readable on all shapes, but on slide 3 the 'Kaheawa Wind Farm' box is bright red instead of green, a clearly wrong color versus the ground truth that also makes an On Track project look identical to the At Risk one.

### Case 69: Cross-Slide Image–Caption Correlation

*Images & Pictures; not in hard subset; wall 176 s; Claude-judged IF 3 / VQ 3; recorded agents mean 0.75, best 2.5.*

**Instruction.** 1. For every slide, match each image to its correct caption.  2. After pairing them, rearrange the pairs to create a balanced layout.  3. Update each slide's title correspondingly. 4. Finally, make sure all images are the same size, 3.2 inches wide by 2.4 inches high.

**Analysis.** Cross-slide image/caption correlation. The agent inspected the embedded PNGs (and their alt-text descriptors) and moved three pictures across slides to pair them with captions, resized all nine to 3.2x2.4 in and laid them out in a 3-column grid. Recorded agents scored 0-2 here, mostly because they did not move pictures across slides. The two deductions are (a) the title edit: the agent appended 'Images & Captions (Matched)' where the ground truth stripped the suffix entirely, and (b) grid layout differing from the ground truth. Notably the ground-truth render has two captions overlapping on slide 1 while the prediction is clean, so this case illustrates ground-truth-anchored judging penalising a better layout.

**Judge reasons (Claude-judged).** IF: Prediction correctly pairs every image with its caption (moving pictures across slides as needed), resizes all pictures to 3.2x2.4 in, and arranges them in a balanced 3-column grid with unaltered caption text, but the title edit is wrong: it replaces the suffix with ' — Images & Captions (Matched)' instead of stripping it to the bare topic ('Ancient Civilizations', 'Core STEM Concepts', 'Space & Exploration') as the ground truth does. VQ: Rendered slides are clean and legible with correctly matched image/caption groups, uniform image sizes and no overlaps, but they visibly differ from the ground truth in the long retained title suffix, a different grid arrangement, and captions narrowed to 3.2 in so they wrap onto two or three lines.

### Case 94: Slide Size Conversion 4:3 → 16:9

*Slide Layout & Placeholders; not in hard subset; wall 136 s; Claude-judged IF 4 / VQ 3; recorded agents mean 1.19, best 3.0.*

**Instruction.** Convert this 4:3 presentation to a 16:9 widescreen format. Make sure all the content fits on the slides and that images are not stretched or distorted.

**Analysis.** Layout: 4:3 to 16:9. The agent rewrote presentation.xml plus master, layouts and slides via lxml (no python-pptx re-save), scaling x/width by 4/3 and shifting but not resizing pictures. All content fits, nothing is stretched. Deviations: it chose 13.33x7.5 in where the ground truth chose 10x5.63 in (both 16:9), so text looks smaller on the larger canvas; the slide-3 chart frame was scaled to 3:1 instead of being kept near 2:1. Recorded agents mostly scored 1/1 (several left the deck at 4:3 or stretched images), so this is a clear improvement; the remaining issue is aesthetic judgement about which elements should scale and which should keep aspect.

**Judge reasons (Claude-judged).** IF: Prediction converts the deck to a true 16:9 size (13.33x7.5in vs GT 10x5.62in), keeps all text/fonts/chart data and legend, moves every '[1]' reference box up inside the slide, and keeps both slide-4 picture aspect ratios (1.78 and ~1.0) intact without overlap, but it stretches the slide-3 chart frame from a 2:1 to a 3:1 aspect and leaves both slide-4 pictures sharing the name 'Picture 2', small deviations from the GT outcome. VQ: All prediction slides render cleanly with no overlap or cut-off content and preserved fonts/colors, but relative to GT the body text and title appear noticeably smaller on the larger canvas, the slide-3 chart is much wider with more empty space below it, and the slide-4 images are enlarged with the caption pushed to the bottom edge, giving visibly different proportions.

### Case 95: Master & Layout Rebind

*Template & Master-Level Edits; not in hard subset; wall 122 s; Claude-judged IF 5 / VQ 3; recorded agents mean 1.12, best 2.5.*

**Instruction.** On slide 2, change the layout from 'Title Slide' to 'Title and Content'. Make sure the existing text content is moved into the new content placeholder.

**Analysis.** Master/layout rebind. The agent edited slide2.xml.rels to point at the 'Title and Content' layout, converted the ctrTitle/subTitle placeholders into title/body placeholders and moved the floating text box's paragraphs into the body placeholder, then removed the orphan text box. Structure matches the ground truth (Claude-judged IF 5). Recorded agents scored IF 3 and VQ 1-2. The VQ deduction comes from slide 3, which the ground truth also touched (moved a picture down to clear overlapping body text) even though the instruction only mentions slide 2; the agent preserved slide 3 as instructed. This is a ground-truth scope mismatch, not an agent failure.

**Judge reasons (Claude-judged).** IF: The prediction, like the ground truth, switches slide 2 to the 'Title and Content' layout with the three JWST bullet paragraphs moved into 'Content Placeholder 2', removes the empty Subtitle placeholder and old TextBox 3, keeps the image and '[1]' citation, and leaves slides 1, 3 and 4 structurally untouched (the only diffs are the narrower 5.5in placeholder width/picture position on slide 2 and the optional slide-3 image shift the GT made). VQ: Slides 1 and 4 are pixel-identical to the ground truth and slide 2 shows the bullets in a balanced left column beside the image with no overlap (text wraps narrower and the picture sits higher than in GT), but slide 3 in the prediction retains the image overlapping the right end of the body-text lines whereas the GT moved the image down to clear it.

### Case 54: Match Slide Deck Theme

*Theme & Background; hard subset; wall 208 s; Claude-judged IF 3 / VQ 3; recorded agents mean 1.25, best 2.0.*

**Instruction.** Apply the layout from slide 2 to all subsequent slides (3 through 9). Make sure the existing text and images are adjusted to fit the new layout.

**Analysis.** Theme/layout propagation (hard subset). The agent re-bound slides 3-9 to slide 2's 'Title and Content' layout at the OOXML level, converting loose text boxes and orphan placeholders into layout-bound title/body placeholders and moving pictures into the right-hand column. Recorded agents all scored 2/1-2 here. Deductions: slide 5 had no title, so the agent promoted the first bullet into the title where the ground truth invented a new title ('Rootmotion vs. controlled movement'); the narrower text column increases wrapping; two screenshots on slide 7 are in the opposite order. The first judge run also penalised 'stripped animations', which is a judge error: the original deck has no animations and only the ground truth gained timing nodes (see the corrected re-run score). Failure type: layout taste plus a judge-input artefact.

**Judge reasons (Claude-judged).** IF: Slides 3-9 all gained TITLE/OBJECT placeholders with text and images carried over like the ground truth, but on slide 5 the prediction promoted the body line 'What is Root Motion?' into the title (dropping it from the body) instead of adding a new title and preserving all body text, slide 7's two pictures were swapped left/right, and animations were stripped from every slide including slides 1-2 which were supposed to remain unchanged. VQ: Prediction slides 3-9 are clean, legible and overlap-free with images right-aligned beside a half-width text column (slides 1-2 are pixel-identical to GT), but the narrower text box causes heavier wrapping than GT (slide 4 title now wraps to two lines, slides 4/7/8/9 bullets wrap), slide 5 lost the 'What is Root Motion?' bullet from the body, and slide 7's screenshot order is reversed.

### Case 50: Normalize Date Format

*Tables; hard subset; wall 151 s; Claude-judged IF 3 / VQ 4; recorded agents mean 0.88, best 1.5.*

**Instruction.** Go through the presentation and standardize all the date formats to 'Month Day, Year', for example 'March 22, 2022'. Make sure to handle different formats like '28 March 2022', '02/26/2022', and '18 of March 2022'.

**Analysis.** Tables / text normalisation across 15 slides. The agent converted 30 dates across nine input formats, including dates split across runs and DD/MM vs MM/DD disambiguation from context, while preserving fonts and layout (Claude-judged VQ 4; recorded agents scored 0-2 on VQ, typically because they rewrote text frames and lost formatting). The IF deduction is a scope judgement: year-less mentions ('February 24', 'March 2') were deliberately left alone, whereas the ground truth completed them to 2022; and 'march' was capitalised. Failure type: conservative instruction interpretation rather than perception or tooling.

**Judge reasons (Claude-judged).** IF: The prediction correctly reformatted every explicitly formatted date (e.g. '25 February 2022', '5 march 2022', '03/28/2022', '24/02/2022', '18 of March 2022', '12 March 2022', '29 October 1998', footer '22 March 2022') to 'Month Day, Year' with fonts/sizes preserved, but unlike the ground truth it left the year-less dates unchanged ('Effective March 2,' on slide 8 and four occurrences of 'February 24'/'March 2' without a year on slide 7, which the ground truth completed to '..., 2022'), and it capitalized 'march' on slide 3 instead of preserving the original lowercase casing. VQ: All 15 prediction slides match the ground truth in layout, fonts, sizes, colors and positions with no unintended changes; the only visible differences are the missing ', 2022' after 'February 24'/'March 2' on slides 7 and 8 (causing slight line-wrap shifts on slide 7) and an en dash vs hyphen between the two 1999 dates on slide 14.

### Case 83: Bibliography Slide from Footers

*Slide/Section Management & Footers; not in hard subset; wall 158 s; Claude-judged IF 3 / VQ 3; recorded agents mean 1.12, best 3.0.*

**Instruction.** Find all the source citations from the bottom of my slides, and create a new 'Bibliography' slide just before the final slide. The new slide should list all unique sources, alphabetized.

**Analysis.** Cross-slide structure: bibliography from footers. The agent found the same 9 unique sources as the ground truth, de-duplicated repeats, alphabetised them and inserted the slide in the right position using the deck's own layout (recorded agents: IF 0-3, several produced no slide or wrong position). The deductions are formatting fidelity: it re-typed the citations as plain 11pt text instead of copying the footer runs, so journal-name italics were lost, one citation was reformatted ('M. Ali and C. Mangione' to 'Ali M, Mangione C'), and the layout's slide-number placeholder was not instantiated. Failure type: rebuild-instead-of-copy, a tooling habit (building new text with python-pptx) rather than perception.

**Judge reasons (Claude-judged).** IF: The prediction inserts a 'Bibliography' slide before the final slide with all 9 unique citations alphabetized like the ground truth, but it drops the italic formatting on journal names (9 runs vs 27, no italics), rewrites citation text ('M. Ali and C. Mangione' -> 'Ali M, Mangione C', adds '(Unpublished Data)'), and omits the slide-number placeholder the ground truth slide carries. VQ: Slides 1-22 and the final 'Thank you' slide render identically to the ground truth, but the new Bibliography slide uses a visibly smaller 11pt font instead of 14pt, lacks the italicized journal names, has no slide number in the corner, and leaves a large empty area below the list.

### Case 67: WCAG Accessibility & Master Cleanup

*Accessibility & Semantics; hard subset; wall 236 s; Claude-judged IF 2 / VQ 2; recorded agents mean 1.44, best 2.5.*

**Instruction.** Improve this presentation's accessibility for screen readers. Ensure every slide has a unique title, the reading order is logical, and all text uses the theme's default font.

**Analysis.** Accessibility and master cleanup (hard subset; every recorded agent scored IF 0-1). The agent converted each slide's heading box into a real title placeholder, rewrote slides 1-4's identical headings into distinct titles, reordered the spTree so titles are read first, and replaced DM Sans/Calibri overrides with Arial on slides, layouts and master. The ground truth took a different route: it added hidden off-slide 'Slide N Title' text boxes, left the visible headings alone and removed font-family overrides entirely so text inherits the theme. The judge therefore penalised the visible title rewrite as an unrequested content change and the explicit Arial overrides as 'not removed'. Failure type: instruction interpretation (what counts as a 'unique title' and 'uses the theme font') on an under-specified task; the agent's reading is defensible for screen readers but diverges from the reference, which is why this case is hard for everyone.

**Judge reasons (Claude-judged).** IF: Prediction achieved unique titles only by rewriting the visible title text on slides 1-4 (e.g. 'TABLE SMARTART INFOGRAPHIC' -> 'IDEA BOARD INFOGRAPHIC', 'TABLE INFOGRAPHIC', 'SMARTART INFOGRAPHIC', 'MAIN POINTS INFOGRAPHIC') instead of adding hidden titles as in ground truth, and it did not remove font overrides at all: every 'DM Sans' run was replaced with an explicit 'Arial' override and the existing 'Arial' overrides on slides 5-6 were left in place, whereas ground truth has no font-family overrides on any text; reading order (title first, then column-wise content) is acceptable. VQ: Slides 1-4 show altered on-screen title text compared with ground truth ('IDEA BOARD INFOGRAPHIC', 'TABLE INFOGRAPHIC', 'SMARTART INFOGRAPHIC', 'MAIN POINTS INFOGRAPHIC' vs 'TABLE SMARTART INFOGRAPHIC'), a clear unrequested content change, while all other elements, fonts, colors, positions and slides 5-6 match the ground truth.


### Cross-cutting notes

- **Ground truth quality.** In Case 69 the ground-truth render has two captions overlapping each other on slide 1 while the prediction is clean; in Case 54 the ground truth invents a new slide title not derivable from the deck; in Case 67 the ground truth adds hidden off-slide text boxes as "titles"; in Case 95 the ground truth also moved a picture on a slide the instruction does not mention. A ground-truth-anchored judge penalises a reasonable edit in each of these. For the financing-deck benchmark this argues for rubric-based checks (does the chart have the right series, is nothing overlapping) rather than a single reference deck.
- **Where recorded agents lose points that this run did not:** editing inside chart caches and embedded workbooks (Case 7), moving pictures across slides (Case 69), rebinding layouts at the rels level (Cases 54, 95), rewriting the master and all layouts for a size change (Case 94), and executing all sub-edits of a long instruction (Case 93). These are tooling-depth differences, and they are the edits that matter for a financing deck.
- **Where this run still loses points:** post-edit layout verification (legend boxes, wrapping), reuse of in-deck style conventions, and judgement calls on ambiguous wording. These are process fixes (render, compare, fix) rather than capability gaps.

## 6. Reproduction

Everything below ran on 4 CPUs / 15 GB with LibreOffice, `pdftoppm`, python-pptx 1.0.2 and Claude Code 2.1.296. Paths assume the layout used here; adjust the constants at the top of each script.

```bash
# 1. Clone the benchmark OUTSIDE this repo (about 1.1 GB; treat as untrusted data)
mkdir -p /home/user/bench && cd /home/user/bench
git clone --depth 1 https://github.com/michaelofengenden/PPTArena.git

# 2. Inventory: per-case table of recorded scores (writes /home/user/bench/work/case_table.json)
#    The aggregation is the inline python in this README's section 2; the same logic is in scripts/assemble.py
#    (leaderboard columns) and was used to produce the appendix table.

# 3. Prepare isolated workdirs and reference renders for the chosen cases
python3 -I scripts/prep_cases.py 7 30 93 98 69 94 95 54 50 83 67
#    -> /home/user/bench/work/runs/case_NNN/{deck.pptx,INSTRUCTION.md}  and  /home/user/bench/work/ref/case_NNN/{orig,gt}/*.png

# 4. Run the agent in each workdir. Intended leaderboard invocation (refused by this session's permission classifier):
#    cd /home/user/bench/work/runs/case_007 && date +%s > .started && \
#    env IS_SANDBOX=1 claude -p "$(cat <<'P'
#    You are completing one case of the PPTArena benchmark (PowerPoint editing).
#    Read INSTRUCTION.md in the current directory, then edit deck.pptx IN PLACE so that it satisfies the instruction.
#    Rules: modify deck.pptx directly and keep the filename; apply the edit to the existing deck; preserve everything
#    the instruction does not ask you to change; verify deck.pptx still opens without repair. Finally run: date +%s > .finished
#    P
#    )" --dangerously-skip-permissions
#    What was actually run: the same prompt text given to a Claude Code general-purpose subagent of the orchestrating
#    session, with the workdir path spelled out and a ban on reading /home/user/bench/PPTArena.

# 5. Collect: validity, render, structural diffs (writes /home/user/bench/work/collected/case_NNN/)
python3 -I scripts/collect.py case_007 case_030 case_093 case_098 case_069 case_094 case_095 case_054 case_050 case_083 case_067

# 6. Build judge prompts, then give each judge_prompt.md to a fresh Claude Code agent that can Read PNGs
python3 -I scripts/build_judge_prompt.py case_007   # repeat per case -> collected/case_NNN/judge_prompt.md -> judge.json

# 7. Merge everything into results.json
python3 -I scripts/assemble.py
```

The agent reports (what each run says it changed) are embedded in `results.json` under `agent_report`. No pptx files, renders or benchmark data are committed.

## 7. Caveats

- Scores are Claude-judged (single sample) and are not comparable in absolute terms with the Kimi-judged leaderboard; the Claude judge may be more lenient on visual quality. A proper comparison needs the same judge on both sets of predictions, which requires an API key for Kimi, Gemini or OpenAI; none was available and `huggingface.co`, `arxiv.org` and `api.openai.com` are blocked by this environment's network policy.
- The agent under test is a Claude Code subagent on this session's model, not the `claude -p` process with `claude-opus-4-8` registered in `agents.json`. The permission classifier refused the nested CLI launch twice (blanket skip and a scoped allowlist).
- Eleven cases, one run each, no repeats; subagent runs are not deterministic.
- The agents could in principle read the ground-truth decks on disk. They were instructed not to, and their reports describe only workdir files, but this was not enforced by a sandbox.
- The structural diff used for judging is this repo's own python-pptx summary (`scripts/collect.py`), not PPTArena's `ppt_processor.diff_pptx_json`; the PPTArena diff code was not executed because the clone is untrusted downloaded data.
- Wall time includes subagent start-up and the agent's own rendering checks.

## Appendix: the 46-case failing set with recorded per-agent IF/VQ (Kimi K2.6 judge, median of 3)

| Case | Edit type | Subset | codex_gpt55 | claude_code_opus48 | gemini_cli_35flash | oc_deepseek_v4 | oc_glm52 | oc_kimi_k27code | oc_minimax_m3 | baidu_dumate_pptx_skill_r266 | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Case 97: LaTeX to Office Math (OMML) | Text & Typography | yes | 0/2 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/1 | 1/1 | 0.31 |
| Case 38: Flip Theme Scheme | Theme & Background |  | 1/1 | 1/1 | 1/1 | 1/1 | 0/0 | 0/0 | 0/0 | 1/1 | 0.62 |
| Case 19: Translate Chinese | Text & Typography |  | 2/3 | 2/1 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 0.75 |
| Case 69: Cross-Slide Image–Caption Correlation | Images & Pictures |  | 2/3 | 1/1 | 1/1 | 0/0 | 0/0 | 0/0 | 0/0 | 1/2 | 0.75 |
| Case 72: Dynamic SmartArt Timeline with Image In | SmartArt & Diagrams |  | 4/3 | 1/2 | 1/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1/0 | 0.75 |
| Case 88: Normalize images and objects on slides | Alignment, Distribution & Z-order |  | 2/1 | 2/1 | 2/1 | 0/0 | 0/0 | 0/0 | 0/0 | 2/1 | 0.75 |
| Case 50: Normalize Date Format | Tables | yes | 1/1 | 1/1 | 1/1 | 1/0 | 1/1 | 0/0 | 1/1 | 1/2 | 0.88 |
| Case 80: Update theme and slides backgrounds(A) | Theme & Background |  | 1/2 | 2/2 | 2/2 | 0/0 | 0/0 | 0/0 | 0/0 | 2/2 | 0.94 |
| Case 4: Increase Font Size on Slide 8 | Text & Typography |  | 3/0 | 3/0 | 3/0 | 0/0 | 2/0 | 0/0 | 3/0 | 3/0 | 1.06 |
| Case 85: Arabic Translate LTR | Text & Typography |  | 2/3 | 2/3 | 2/2 | 0/0 | 0/0 | 0/0 | 0/0 | 2/1 | 1.06 |
| Case 83: Bibliography Slide from Footers | Slide/Section Management & Footers |  | 3/3 | 2/2 | 2/0 | 0/0 | 0/0 | 0/0 | 2/0 | 2/2 | 1.12 |
| Case 93: Multi-Edit Cascade (Copernicus Climate  | Charts |  | 3/3 | 2/2 | 2/2 | 0/0 | 0/0 | 0/0 | 0/0 | 1/3 | 1.12 |
| Case 95: Master & Layout Rebind | Template & Master-Level Edits |  | 3/1 | 3/2 | 3/1 | 0/0 | 0/0 | 0/0 | 0/0 | 3/2 | 1.12 |
| Case 45: Lighter Colors | Theme & Background |  | 2/1 | 2/1 | 2/2 | 2/1 | 0/0 | 2/1 | 0/0 | 2/1 | 1.19 |
| Case 94: Slide Size Conversion 4:3 → 16:9 | Slide Layout & Placeholders |  | 2/4 | 1/1 | 1/1 | 0/0 | 0/0 | 1/3 | 0/0 | 1/4 | 1.19 |
| Case 43: Transitionary Slides | Slide/Section Management & Footers |  | 2/1 | 1/2 | 0/0 | 1/2 | 2/2 | 0/0 | 2/1 | 2/2 | 1.25 |
| Case 54: Match Slide Deck Theme | Theme & Background | yes | 2/2 | 2/1 | 2/1 | 2/1 | 2/1 | 0/0 | 0/0 | 2/2 | 1.25 |
| Case 1: Translate to English But Keep French | Text & Typography |  | 1/0 | 2/0 | 2/1 | 2/1 | 2/1 | 2/0 | 1/1 | 2/3 | 1.31 |
| Case 34: Lambda Replacement | Text & Typography | yes | 1/1 | 2/1 | 2/1 | 1/1 | 2/0 | 2/1 | 0/0 | 2/4 | 1.31 |
| Case 76: Aesthetic Slide Makeover | Theme & Background |  | 3/3 | 2/2 | 2/2 | 2/1 | 0/0 | 0/0 | 0/0 | 2/2 | 1.31 |
| Case 77: Educational Solar System Makeover | Theme & Background |  | 2/2 | 3/1 | 3/2 | 0/0 | 0/0 | 3/1 | 0/0 | 2/2 | 1.31 |
| Case 96: Reading Order Fix (Complex Slides) | Accessibility & Semantics |  | 2/4 | 2/1 | 2/2 | 0/0 | 0/0 | 2/3 | 0/0 | 2/1 | 1.31 |
| Case 98: Cross-Slide Conditional Formatting (Sta | SmartArt & Diagrams |  | 2/2 | 2/2 | 3/2 | 0/0 | 0/0 | 2/2 | 0/0 | 2/2 | 1.31 |
| Case 39: Generate Conclusion Slide | Slide/Section Management & Footers |  | 1/3 | 1/2 | 1/3 | 1/2 | 0/0 | 0/0 | 1/2 | 1/4 | 1.38 |
| Case 90: Screenshot-to-Editable Text (UB Title S | Slide Layout & Placeholders |  | 1/5 | 1/5 | 1/4 | 0/0 | 0/0 | 0/0 | 0/0 | 1/4 | 1.38 |
| Case 67: WCAG Accessibility & Master Cleanup | Accessibility & Semantics | yes | 1/4 | 1/4 | 1/2 | 1/2 | 0/2 | 0/0 | 0/0 | 1/4 | 1.44 |
| Case 35: Structural Fix | Text & Typography | yes | 2/0 | 2/1 | 2/1 | 1/1 | 2/1 | 2/1 | 1/1 | 2/4 | 1.50 |
| Case 46: Convert Text & Arrows to SmartArt | SmartArt & Diagrams | yes | 2/2 | 2/2 | 3/2 | 2/2 | 2/1 | 0/0 | 0/0 | 2/2 | 1.50 |
| Case 7: Update Quarter Two Data (B) | Charts | yes | 2/2 | 1/2 | 1/1 | 1/2 | 1/2 | 1/2 | 1/1 | 1/4 | 1.56 |
| Case 89: Fill in Animal Research poster | Text & Typography | yes | 2/2 | 2/2 | 1/2 | 1/2 | 2/2 | 2/2 | 0/0 | 1/2 | 1.56 |
| Case 92: Avatar Circle Crop | Images & Pictures | yes | 1/2 | 1/2 | 1/0 | 1/4 | 2/2 | 1/2 | 1/2 | 1/2 | 1.56 |
| Case 6: Update Quarter Two Data (A) | Charts | yes | 1/1 | 2/1 | 2/1 | 2/1 | 2/1 | 2/1 | 2/1 | 2/4 | 1.62 |
| Case 40: Hindu Center Titles | Text & Typography | yes | 2/2 | 1/1 | 2/2 | 2/1 | 1/1 | 2/2 | 2/0 | 3/3 | 1.69 |
| Case 44: Match Flag to Text | Images & Pictures | yes | 1/4 | 1/1 | 2/4 | 1/3 | 1/1 | 2/4 | 0/0 | 2/1 | 1.75 |
| Case 12: Stock Photo Cleanup | Text & Typography | yes | 2/2 | 2/2 | 2/3 | 1/2 | 2/2 | 1/2 | 2/2 | 2/2 | 1.94 |
| Case 53: Fill Table from Data | Tables | yes | 1/3 | 2/2 | 1/2 | 1/3 | 2/2 | 1/4 | 2/2 | 1/2 | 1.94 |
| Case 57: Add Water Mark | Shapes & Drawing | yes | 3/1 | 3/0 | 3/1 | 0/1 | 4/1 | 1/0 | 4/1 | 4/4 | 1.94 |
| Case 30: Convert Text Data to a Line Chart | Charts | yes | 4/0 | 3/0 | 4/1 | 3/0 | 4/2 | 4/0 | 3/0 | 3/3 | 2.12 |
| Case 21: Title Case Titles | Text & Typography | yes | 4/1 | 4/1 | 3/0 | 4/0 | 4/1 | 3/1 | 2/2 | 2/3 | 2.19 |
| Case 16: Curate Multi-Panel Photo Layout | Alignment, Distribution & Z-order | yes | 2/4 | 3/4 | 2/2 | 2/1 | 2/2 | 2/4 | 0/0 | 3/4 | 2.31 |
| Case 28: Fix Slide Order and Agenda | Slide/Section Management & Footers | yes | 0/1 | 2/5 | 5/4 | 1/2 | 2/4 | 1/2 | 0/2 | 4/5 | 2.50 |
| Case 17: Build Ensemble Category Boards | Shapes & Drawing | yes | 1/4 | 2/4 | 2/4 | 1/2 | 2/3 | 2/4 | 1/4 | 2/4 | 2.62 |
| Case 42: Organize Research Poster | Alignment, Distribution & Z-order | yes | 4/4 | 3/2 | 4/3 | 2/2 | 4/4 | 1/2 | 1/2 | 4/2 | 2.75 |
| Case 87: Merge Near-Duplicate Slides | Slide/Section Management & Footers | yes | 5/0 | 5/2 | 5/2 | 5/1 | 5/1 | 5/2 | 5/1 | 5/5 | 3.38 |
| Case 27: Correct Images | Images & Pictures | yes | 5/5 | 4/5 | 4/1 | 2/1 | 4/4 | 4/5 | 2/2 | 5/5 | 3.62 |
| Case 47: Change Line Graph to Bar Graph | Charts | yes | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/4 | 4.94 |
