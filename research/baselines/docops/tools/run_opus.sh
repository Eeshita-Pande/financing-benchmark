#!/bin/bash
cd /home/user/bench
export DOCOPS_MODEL=claude-opus-5-5
while read T; do
  [ -z "$T" ] && continue
  echo "START $T off opus $(date +%T)"
  ./venv/bin/python -I tools/run_task.py "$T" off > "runs/${T}__skill_off__opus.log" 2>&1
  echo "END $T off opus $(date +%T) :: $(tail -1 runs/${T}__skill_off__opus.log)"
done < tools/failed_tasks.txt
echo OPUS-DONE
