#!/usr/bin/env python3
"""Aggregate runs/*/summary.json into results.json + a markdown table."""
import json, sys
from pathlib import Path
BENCH = Path('/home/user/bench')
inv = {r['task']: r for r in json.loads((BENCH / 'inventory.json').read_text())}
runs = []
for s in sorted((BENCH / 'runs').glob('*/summary.json')):
    d = json.loads(s.read_text())
    d['level'] = inv[d['task']]['level']
    d['doc_type'] = inv[d['task']]['doc_type']
    runs.append(d)
out = {'runs': runs}
(BENCH / 'results_raw.json').write_text(json.dumps(out, indent=1))
order = [l.strip() for l in (BENCH / 'tools' / 'tasklist.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
print('| task | level | mode | reward | tests passed | wall s | turns | tools | timed out | outputs open |')
print('|---|---|---|---|---|---|---|---|---|---|')
for t in order:
    for mode in ('skill_off', 'skill_on'):
        for d in runs:
            if d['task'] == t and d['mode'] == mode:
                tp = sum(1 for v in d['tests'].values() if v['outcome'] == 'passed')
                opens = ','.join(str(v['opens']) for v in d['files'].values())
                print(f"| {t} | {d['level']} | {mode} | {d['reward']} | {tp}/{len(d['tests'])} | {d['wall_seconds']} | {d['num_turns']} | {d['n_tool_uses']} | {d['timed_out']} | {opens} |")
