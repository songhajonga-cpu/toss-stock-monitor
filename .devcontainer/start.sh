#!/usr/bin/env bash
set -e
cd "$(git rev-parse --show-toplevel)"

python -m pip install -q -r requirements.txt

pkill -f "uvicorn app:app" 2>/dev/null || true

nohup python -m uvicorn app:app --host 0.0.0.0 --port 8000   > /tmp/stock-monitor.log 2>&1 < /dev/null &

for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    exit 0
  fi
  sleep 1
done

cat /tmp/stock-monitor.log || true
exit 1
