import json, sys
from pathlib import Path
for s in sorted(Path('/home/user/bench/runs').glob('*/summary.json')):
    d = json.loads(s.read_text())
    if d['reward'] == 1 and all(v['outcome']=='passed' for v in d['tests'].values()):
        continue
    print(f"\n### {d['task']} [{d['mode']}] reward={d['reward']} wall={d['wall_seconds']}s turns={d['num_turns']} timed_out={d['timed_out']}")
    for k, v in d['files'].items():
        print(f"  file {k}: exists={v['exists']} opens={v['opens']} size={v['size']}")
    for name, t in d['tests'].items():
        if t['outcome'] != 'passed':
            print(f"  FAIL {name}: {t['message'][:600]}")
