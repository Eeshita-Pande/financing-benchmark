#!/usr/bin/env python3
"""Prepare isolated workdirs for selected PPTArena cases (mirrors agent_bench/run_agents.py)."""
import json, shutil, hashlib, sys, os, re, subprocess
from pathlib import Path
REPO = Path('/home/user/bench/PPTArena'); WORK = Path('/home/user/bench/work/runs'); REF = Path('/home/user/bench/work/ref')
CASES = [int(x) for x in sys.argv[1:]]
pairs = {p['name'].strip(): p for p in json.load(open(REPO/'src/evaluation_pairs_refined.json'))}
INSTRUCTION_TEMPLATE = """# PPTArena case: {case_name}

Edit `deck.pptx` (in this directory) according to the instruction below.

## Instruction

{prompt}
"""
def sha(p):
    h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def render(pptx, outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    if list(outdir.glob('*.png')): return sorted(outdir.glob('*.png'))
    subprocess.run(['soffice','--headless','--convert-to','pdf','--outdir',str(outdir),str(pptx)],capture_output=True,timeout=600)
    pdf=next(outdir.glob('*.pdf'),None)
    if not pdf: return []
    subprocess.run(['pdftoppm','-r','60','-png',str(pdf),str(outdir/'slide')],capture_output=True,timeout=600)
    return sorted(outdir.glob('*.png'))
manifest={}
for c in CASES:
    name=[n for n in pairs if n.startswith(f'Case {c}:')][0]; m=pairs[name]
    slug=f'case_{c:03d}'; wd=WORK/slug
    if wd.exists(): shutil.rmtree(wd)
    wd.mkdir(parents=True)
    shutil.copy2(REPO/m['original'], wd/'deck.pptx')
    (wd/'INSTRUCTION.md').write_text(INSTRUCTION_TEMPLATE.format(case_name=name, prompt=m['prompt']))
    # reference renders (original + ground truth), kept outside the workdir
    o=render(REPO/m['original'], REF/slug/'orig'); g=render(REPO/m['ground_truth'], REF/slug/'gt')
    manifest[slug]=dict(name=name, prompt=m['prompt'], style_target=m['style_target'], category=m['category'], edit_type=m.get('edit_type'),
        original=m['original'], ground_truth=m['ground_truth'], original_sha256=sha(wd/'deck.pptx'), workdir=str(wd),
        orig_png=len(o), gt_png=len(g))
    print(slug, name, '| orig pngs', len(o), '| gt pngs', len(g))
json.dump(manifest, open(WORK/'manifest.json','w'), indent=1)
