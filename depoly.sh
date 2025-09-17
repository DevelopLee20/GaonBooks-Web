#!/bin/bash
set -e

APP_NAME="gaonbooks-dev"

# 2. 기존 gunicorn 프로세스 종료 (이름 기준)
echo ">>> 기존 Gunicorn 종료..."
PIDS=$(ps aux | grep "gunicorn app.main:app" | grep "$APP_NAME" | awk '{print $2}')

if [ -n "$PIDS" ]; then
    echo ">>> 프로세스 종료: $PIDS"
    kill -TERM $PIDS
else
    echo ">>> 종료할 프로세스 없음"
fi

# 3. 백엔드 실행
echo ">>> 백엔드(Gunicorn) 실행..."
pipenv run gunicorn app.main:app \
    --name "$APP_NAME" \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile ./gunicorn-access.log \
    --error-logfile ./gunicorn-error.log \
    --capture-output \
    --log-level info \
    --daemon

# 4. 프론트엔드 재시작 (pm2)
echo ">>> 프론트엔드(pm2) 재시작..."
pm2 restart frontend

echo ">>> 배포 완료!"
