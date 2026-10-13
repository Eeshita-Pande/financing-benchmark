import json, sys
for l in open(sys.argv[1]):
    try: r=json.loads(l)
    except: print('RAW', l[:300]); continue
    t=r.get('type')
    if t=='assistant':
        for b in r['message']['content']:
            if b.get('type')=='text': print('TEXT:', b['text'][:800])
            elif b.get('type')=='tool_use': print('TOOL:', b['name'], json.dumps(b['input'])[:int(sys.argv[2]) if len(sys.argv)>2 else 600])
    elif t=='user':
        for b in r['message']['content']:
            if isinstance(b,dict) and b.get('type')=='tool_result': print('RESULT:', str(b.get('content'))[:500])
    elif t=='result': print('RESULT_REC:', r.get('subtype'), 'err=',r.get('is_error'), 'turns=',r.get('num_turns'), 'cost=',r.get('total_cost_usd'), 'models=', list(r.get('modelUsage',{}).keys()))
