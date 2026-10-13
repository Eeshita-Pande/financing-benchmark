#!/usr/bin/env python3
"""Assemble README.md from the draft sections and the tables produced by report.py."""
import json, re
from pathlib import Path
B = Path('/home/user/bench'); D = B / 'draft'
tables = (B / 'results_tables.md').read_text()
main = tables[tables.index('## Main runs'):tables.index('## Model-variant') if '## Model-variant' in tables else tables.index('## Pass rate')]
variant = tables[tables.index('## Model-variant'):tables.index('## Pass rate')] if '## Model-variant' in tables else ''
bylevel = tables[tables.index('## Pass rate'):]
res = json.loads((B / 'results.json').read_text())['runs']
mainruns = [r for r in res if r['model_requested'] == 'cli-default']
def rate(lvl, mode, key):
    ds = [r for r in mainruns if r['level'] == lvl and r['mode'] == mode]
    if key == 'strict': n = sum(r['reward'] for r in ds)
    else: n = sum((r.get('lenient') or {}).get('reward', r['reward']) if (r.get('lenient') or {}).get('applied') else r['reward'] for r in ds)
    return f'{n}/{len(ds)}'
summary = f"""## Summary

* 12 PowerPoint-centred DocOps tasks (2 L1, 3 L3, 7 L4; 5 of the L4 tasks are workbook-to-deck or deck-plus-workbook), each run once skill-off and once skill-on with Claude Code (`claude-sonnet-5-5`), plus opus reruns (`claude-opus-5-5`) of the 8 strict failures. 24 + 7 completed runs, all under the 15 min cap, every output file opened cleanly. Runs were outside Docker.
* Strict pass rate (the task's own verifier, as the official harness would score it): L1 {rate('L1','skill_off','strict')} / {rate('L1','skill_on','strict')}, L3 {rate('L3','skill_off','strict')} / {rate('L3','skill_on','strict')}, L4 {rate('L4','skill_off','strict')} / {rate('L4','skill_on','strict')} (skill-off / skill-on).
* Lenient pass rate (same verifier, pointed at the file the agent actually wrote): L4 {rate('L4','skill_off','lenient')} / {rate('L4','skill_on','lenient')}.
* The gap between strict and lenient is a benchmark defect, not an agent failure: all 40 v2 L4 tasks name their output files differently in the instruction than in the verifier (section 5.1a). Two more of the sampled v2 tasks require sheet names, slide titles, headings and one numeric constant that appear in no input (5.1b), and 33 v2 L3 tasks ship the verifier's expected values into the agent's container (5.1c).
* Opus reruns of the 8 strict failures (skill-off): 1 of 7 completed reruns passed strictly (`pptwf_001`); the eighth (`l4_065`) did not run because the org spend limit was hit. Opus repeated the board-pack slide-order failure exactly and introduced one new content error (`l4_043`, over-redaction inside the internal workbook).
* The genuine, repeatable agent failures are both of one kind: slide-ordering rules stated inside the deck rather than in the brief (`pptwf_001`, `pptxr_001`). Numbers were never wrong, no file was ever corrupted, and skills changed no outcome.
"""
head = (D / 'README_static.md').read_text()
sel = (D / 'README_selection.md').read_text()
intro = ("## 4. Results\n\nStrict reward is 1 only when every test function of the task's verifier passes (this is what `tests/test.sh` writes to `reward.txt`). "
         "\"tests\" is passed/total test functions; v1 tasks have a single function. \"lenient\" re-runs the same verifier after mapping the verifier's expected file names onto the files the agent actually wrote, and is shown only where that mapping was needed. "
         "\"verifier mentions\" counts transcript lines that reference `tests/`, `test_outputs`, `verifier_utils` or `verifier_expectations`; it is 0 for every main run. Per-test outcomes and the first failing assertion for every run are in `results.json`.\n\n")
opus_note = (D / 'README_opus_note.md').read_text() if (D / 'README_opus_note.md').exists() else ''
variant_md = variant.replace('## Model-variant reruns of verifier-failed tasks', 'Opus reruns of the strict failures (skill-off)').strip() if variant else 'Opus reruns\n\n(not yet available)'
results = (intro + '### 4.1 ' + main.replace('## Main runs (CLI default model)', 'All main runs').strip()
           + '\n\n### 4.2 ' + bylevel.replace('## Pass rate by level (main runs)', 'Pass rate by level').strip()
           + '\n\n### 4.3 ' + variant_md + '\n\n' + opus_note + '\n')
analysis = (D / 'README_analysis.md').read_text()
tail = (D / 'README_tail.md').read_text()
# insert summary after the intro paragraph (before '## 1.')
head = head.replace('## 1. Benchmark inventory', summary + '\n## 1. Benchmark inventory')
out = head.rstrip() + '\n\n' + sel.strip() + '\n\n' + results.strip() + '\n\n' + analysis.strip() + '\n\n' + tail.strip() + '\n'
(B / 'README_assembled.md').write_text(out)
print(len(out.splitlines()), 'lines')
