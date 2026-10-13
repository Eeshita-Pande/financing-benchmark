#!/usr/bin/env python3
"""Merge manifest + collected records + Claude-judge scores + recorded leaderboard scores into results.json."""
import json, csv, glob, os, statistics
from pathlib import Path
WORK=Path('/home/user/bench/work'); REPO=Path('/home/user/bench/PPTArena')
manifest=json.load(open(WORK/'runs/manifest.json'))
CLI=['codex_gpt55','claude_code_opus48','gemini_cli_35flash','opencode_deepseek_v4','opencode_glm52','opencode_kimi_k27code','opencode_minimax_m3','baidu_dumate_pptx_skill_r266']
lb={}
for f in sorted(glob.glob(str(REPO/'agent_bench/results/*_judge_results.csv'))):
    agent=os.path.basename(f).replace('_judge_results.csv','')
    for row in csv.DictReader(open(f,encoding='utf-8')):
        try: lb.setdefault(row['case_name'].strip(),{})[agent]={'IF':float(row['instruction_following_score']),'VQ':float(row['visual_quality_score']),'judge':row['judge_model']}
        except: pass
notes=json.load(open(WORK/'analysis_notes.json')) if (WORK/'analysis_notes.json').exists() else {}
out=[]
for slug,m in manifest.items():
    cd=WORK/'collected'/slug
    rec=json.load(open(cd/'record.json')) if (cd/'record.json').exists() else {'status':'not_collected'}
    judge=json.load(open(cd/'judge.json')) if (cd/'judge.json').exists() else None
    rerun=json.load(open(cd/'judge_rerun.json')) if (cd/'judge_rerun.json').exists() else None
    r={'case':m['name'],'slug':slug,'edit_type':m['edit_type'],'category':m['category'],'in_hard_subset':slug in json.load(open(WORK/'subset_slugs.json')) if (WORK/'subset_slugs.json').exists() else None,
       'prompt':m['prompt'],'original':m['original'],'ground_truth':m['ground_truth'],
       'run':{k:rec.get(k) for k in ['status','wall_seconds','sha_changed','is_zip_pptx','python_pptx_opens','renders_with_soffice','n_pred_png','n_slides','slide_size_in','n_charts','n_tables']},
       'agent_report':(cd/'agent_report.md').read_text() if (cd/'agent_report.md').exists() else None,
       'claude_judge':{'label':'Claude-judged (Claude Code subagent, adapted PPTArena arena rubric), NOT the official GPT-5/Gemini/Kimi judge', **(judge or {'error':'no judge output'})},
       'leaderboard_recorded':{a:lb.get(m['name'],{}).get(a) for a in CLI if a in lb.get(m['name'],{})},
       'analysis':notes.get(slug)}
    if rerun: r['claude_judge_rerun_corrected_diff_note']=rerun
    cl=[(v['IF']+v['VQ'])/2 for v in r['leaderboard_recorded'].values()]
    r['leaderboard_mean_combined']=round(statistics.mean(cl),2) if cl else None
    r['leaderboard_best_combined']=round(max(cl),2) if cl else None
    out.append(r)
json.dump({'meta':{'benchmark':'PPTArena (michaelofengenden/PPTArena, cloned 2026-10-13, depth 1)','agent_under_test':'Claude Code subagents of a Claude Code cloud session (general-purpose agent, tools Bash/Read/Write/Edit; same TASK_PROMPT text as agent_bench/run_agents.py)','judge':'Claude Code subagent reading LibreOffice-rendered PNGs plus a python-pptx structural diff; rubric text copied from src/llm/judge.py arena mode. NOT the official judge.','date':'2026-10-13'},'cases':out}, open(WORK/'results.json','w'), indent=1, ensure_ascii=False)
print(f"{'slug':<9}{'status':<8}{'wall':>5} {'IF':>3}{'VQ':>3}  lb_mean lb_best  name")
for r in out:
    j=r['claude_judge']; print(f"{r['slug']:<9}{str(r['run']['status']):<8}{str(r['run']['wall_seconds']):>5} {str(j.get('instruction_following_score','-')):>3}{str(j.get('visual_quality_score','-')):>3}  {r['leaderboard_mean_combined']!s:>7} {r['leaderboard_best_combined']!s:>7}  {r['case'][:50]}")
