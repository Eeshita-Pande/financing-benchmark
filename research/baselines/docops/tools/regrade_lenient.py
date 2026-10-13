#!/usr/bin/env python3
"""Lenient regrade: when a verifier-expected output file is missing but the agent wrote a file of the same
extension under a different (instruction-named) filename in submission/, point a COPY of task_metadata.json
at the file the agent actually wrote and re-run the verifier. Strict results are untouched; the lenient
outcome is stored under summary['lenient'].
"""
import json, re, subprocess, sys
from pathlib import Path
BENCH = Path('/home/user/bench'); VENV = BENCH / 'venv' / 'bin' / 'python'
for s in sorted((BENCH / 'runs').glob('*/summary.json')):
    d = json.loads(s.read_text()); run = s.parent
    if run.name.startswith('_'): continue
    meta_p = run / 'tests' / 'task_metadata.json'
    meta_txt = meta_p.read_text()
    sub = run / 'work' / 'submission'
    remap = {}
    for kind, f in d['files'].items():
        if f['exists']: continue
        exp = Path(f['path'])
        cands = [c for c in sub.glob('*' + exp.suffix) if c.is_file()]
        if len(cands) == 1 and str(exp) in meta_txt:
            remap[str(exp)] = str(cands[0])
    if not remap:
        d['lenient'] = {'applied': False}
        s.write_text(json.dumps(d, indent=1)); continue
    for a, b in remap.items():
        meta_txt = meta_txt.replace(a, b)
    lm = run / 'tests' / 'task_metadata_lenient.json'; lm.write_text(meta_txt)
    meta = json.loads(meta_txt)
    env = dict(__import__('os').environ); env['TASK_METADATA_PATH'] = str(lm)
    env['INPUT_PATH'] = meta.get('input_path', ''); env['OUTPUT_PATH'] = remap.get(meta.get('output_path', ''), meta.get('output_path', ''))
    rep = run / 'pytest_report_lenient.json'
    g = subprocess.run([str(VENV), '-I', '-m', 'pytest', str(run / 'tests' / 'test_outputs.py'), '-rA', '-v', '-p', 'no:cacheprovider',
                        '--json-report', f'--json-report-file={rep}'], cwd=run / 'tests', env=env, capture_output=True, text=True, timeout=600)
    (run / 'pytest_output_lenient.txt').write_text(g.stdout + g.stderr)
    tests = {}
    r = json.loads(rep.read_text())
    for t in r.get('tests', []):
        msg = ''
        if t['outcome'] != 'passed':
            cr = t.get('call') or t.get('setup') or {}
            msg = (cr.get('crash') or {}).get('message', '') or (cr.get('longrepr', '') or '')[-800:]
        tests[t['nodeid'].split('::')[-1]] = {'outcome': t['outcome'], 'message': msg[:800]}
    reward = 1 if r['summary'].get('passed', 0) == r['summary'].get('total', 0) > 0 else 0
    d['lenient'] = {'applied': True, 'remap': remap, 'tests': tests, 'reward': reward}
    s.write_text(json.dumps(d, indent=1))
    print(run.name, 'lenient reward', reward, {k: v['outcome'] for k, v in tests.items()})
