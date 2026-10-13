#!/usr/bin/env python3
"""Build the judge prompt for a collected case (adapted from PPTArena src/llm/judge.py arena mode)."""
import json, sys
from pathlib import Path
WORK=Path('/home/user/bench/work'); manifest=json.load(open(WORK/'runs/manifest.json'))
RUBRIC_IF = """HARSH SCORING POLICY (very strict):
- Choose the lower score when uncertain between adjacent scores.
- For translation/summarization or other text edits requiring reasoning, semantic similarity is more important than exact wording.

INSTRUCTION_FOLLOWING score (0-5):
- 5: Every requested object/change exists and is exactly correct; nothing requested is missing or misapplied; no extra edits beyond the instruction.
- 4: All requested changes exist and are mostly correct; only a tiny inaccuracy that does not affect meaning.
- 3: Most requested changes exist but at least one is incomplete, incorrect, or missing detail.
- 2: Only some requested changes exist; notable misses or incorrect applications.
- 1: Requested changes largely not performed or substantially incorrect.
- 0: Contradicts or ignores the instruction entirely."""
RUBRIC_VQ = """HARSH SCORING POLICY (very strict):
- Penalize any unintended visual change to non-requested content (fonts, sizes, colors, positions, shapes, charts, images, tables, or slide structure).
- Choose the lower score when uncertain between adjacent scores.

VISUAL_Quality score (0-5):
- 5: No unintended changes to non-requested content; fonts, sizes, colors, positions, and objects match Ground Truth; structure preserved.
- 4: Visually very close to the Ground Truth; only imperceptible or negligible differences (e.g., sub-pixel alignment); no style drift.
- 3: Minor but noticeable visual differences (e.g., slight font weight/size/spacing shifts) without breaking layout.
- 2: Clear deviations (e.g., wrong fonts/sizes/colors, noticeable position shifts) or small layout issues.
- 1: Major deviations (overlap, off-canvas, broken layout) but still legible.
- 0: Severely broken or unreadable slide."""
slug=sys.argv[1]; m=manifest[slug]; cd=WORK/'collected'/slug
diff=(cd/'diff_gt_vs_pred.txt').read_text()[:14000]
gt=sorted(str(p) for p in (WORK/'ref'/slug/'gt').glob('*.png')); pred=sorted(str(p) for p in (cd/'pred').glob('*.png'))
out=f"""You are the judge for one case of the PPTArena benchmark (PowerPoint editing). You will produce TWO independent scores, following the official PPTArena arena-judge protocol as closely as possible. Do not edit any files except the one JSON output file named at the end. Do not read anything under /home/user/bench/PPTArena.

--- USER INSTRUCTION (what the editing agent received) ---
{m['prompt']}

--- STYLE TARGET (your evaluation rubric - the editing agent DID NOT see this) ---
{m['style_target']}

==================== PART 1: INSTRUCTION FOLLOWING (structural diff only) ====================
You are a strict judge of INSTRUCTION FOLLOWING.

CRITICAL UNDERSTANDING:
- The "Instruction" is what the model/editor received (the user's request)
- The "Style Target" is YOUR evaluation rubric - the model DID NOT see this
- You will receive a FOCUSED DIFF showing only what differs between ground_truth and prediction (shape-level JSON extracted with python-pptx: text, fonts, positions in inches, fills, chart series, table cells, layouts)
- Your job: Judge if the prediction's changes match the ground_truth's changes
- DO NOT compare prediction to initial - focus on whether prediction achieved ground_truth's outcome
- If the diff shows minimal differences, that's GOOD (high score)
- Ground Truth is ONE valid example, not the only correct answer

FLEXIBILITY:
- Accept different valid approaches (e.g., flags in a list vs rows is fine if they match the text)
- Exact positions/sizes don't matter unless the Instruction explicitly requires them
- Very small measurement variations (±1%) are acceptable for fonts/sizes due to rounding
- Z-order (layering) differences ARE significant and should be noted
- Focus on semantic properties: text content, font names, colors, structural changes, z-order

{RUBRIC_IF}

--- FOCUSED DIFF (GROUND_TRUTH vs PREDICTION; a shape listed under one label only is one whose properties differ from the other deck) ---
{diff}

(The full per-deck shape summaries are in {cd/'summaries.json'} and the ORIGINAL-vs-PREDICTION diff is in {cd/'diff_orig_vs_pred.txt'} if you need more detail.)

==================== PART 2: VISUAL QUALITY (slide images only) ====================
You are a judge of VISUAL/CONTENT QUALITY and PRESERVATION.

CRITICAL UNDERSTANDING:
- The "Instruction" is what the model/editor received
- The "Style Target" is YOUR evaluation rubric - the model DID NOT see this
- Ground Truth is ONE valid example - accept other valid visual approaches
- Focus on SEMANTIC correctness: Are the visual elements correct? No overlap? Readable?
- Exact positions/sizes don't matter unless the Instruction explicitly requires them
- You will only receive Ground Truth and Prediction slide images; compare them directly slide-by-slide.
- Use any provided Style Target guidance to check required visual cues strictly.

FLEXIBILITY:
- Different layouts achieving the same goal are acceptable (e.g., list vs grid)
- Small position variations are fine if elements are clear and non-overlapping
- Theme colors may vary slightly as long as they're harmonious
- "Approximately centered" or "well-aligned" is acceptable without pixel-perfection

{RUBRIC_VQ}

Slide images (PNG, rendered with LibreOffice; read every one of them with the Read tool):
GROUND_TRUTH ({len(gt)} slides):
""" + "\n".join(f"  GROUND_TRUTH_SLIDE_{i+1}: {p}" for i,p in enumerate(gt)) + f"""
PREDICTION ({len(pred)} slides):
""" + "\n".join(f"  PREDICTION_SLIDE_{i+1}: {p}" for i,p in enumerate(pred)) + f"""

Judge visual quality by comparing PREDICTION to GROUND TRUTH.

==================== OUTPUT ====================
Write a single JSON object to {cd/'judge.json'} with exactly these keys:
- instruction_following_score (0-5, integer)
- instruction_following_reason (one sentence, specific evidence comparing prediction to ground_truth)
- visual_quality_score (0-5, integer)
- visual_quality_reason (one sentence, specific evidence about visual differences)
Then reply with the same JSON.
"""
(cd/'judge_prompt.md').write_text(out); print(cd/'judge_prompt.md', len(out), 'chars;', len(gt), 'gt png,', len(pred), 'pred png')
