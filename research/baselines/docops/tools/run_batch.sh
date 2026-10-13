#!/bin/bash
# usage: run_batch.sh MODE [PARALLEL]  -- runs every task in tasklist.txt (skipping ones already done)
MODE=$1; P=${2:-3}
cd /home/user/bench
grep -v '^#' tools/tasklist.txt | while read T; do
  [ -z "$T" ] && continue
  if [ -f "runs/${T}__skill_${MODE}/summary.json" ]; then echo "skip $T $MODE (done)" >&2; continue; fi
  echo "$T"
done | xargs -P 1 -I{} bash -c 'echo "START {} '"$MODE"' $(date +%T)"; ./venv/bin/python -I tools/run_task.py {} '"$MODE"' > runs/{}__skill_'"$MODE"'.log 2>&1; echo "END {} '"$MODE"' $(date +%T) :: $(tail -1 runs/{}__skill_'"$MODE"'.log)"'
