import json, sys, tomllib, re
from pathlib import Path
tasks = Path(sys.argv[1])
rows = []
for d in sorted(p for p in tasks.iterdir() if (p/'task.toml').is_file()):
    t = tomllib.loads((d/'task.toml').read_text())
    m = t.get('metadata', {})
    level = m.get('final_difficulty') or re.match(r'L\d', str(m.get('difficulty_level',''))).group(0)
    meta = json.loads((d/'tests'/'task_metadata.json').read_text())
    summary = meta.get('user_task_description') or meta.get('single_step_benchmark_instruction') or ''
    summary = ' '.join(summary.split())
    if len(summary) > 140: summary = summary[:137] + '...'
    outs = meta.get('output_paths') or {'main': meta.get('output_path')}
    rows.append(dict(task=d.name, level=level, doc_type=meta.get('doc_type', m.get('doc_type','')),
        modality=meta.get('primary_modality',''), summary=summary,
        n_outputs=len(outs), outputs=outs, input_path=meta.get('input_path'),
        supporting=meta.get('supporting_input_paths', []),
        agent_timeout=t.get('agent',{}).get('timeout_sec'),
        verifier_mode=meta.get('verifier_mode','')))
json.dump(rows, open(sys.argv[2],'w'), indent=1)
from collections import Counter
print(Counter((r['level'], r['doc_type']) for r in rows))
