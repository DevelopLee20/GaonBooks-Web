#!/bin/bash
set -e

# Add user's local bin to path to find pipenv
export PATH="$HOME/.local/bin:$PATH"

# Navigate to the project directory
cd ~/GaonBooks-Web || exit

# Update source code
git checkout master
git reset --hard HEAD
git pull origin master

# Backend Deployment
echo "--- Deploying Backend ---"
pipenv sync
pkill -f "gunicorn app.main:app" || true
pipenv run gunicorn app.main:app \
    --name gaonbooks-dev \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile ./gunicorn-access.log \
    --error-logfile ./gunicorn-error.log \
    --capture-output \
    --log-level info \
    --daemon
echo "Backend deployment command issued."

# Frontend Deployment
echo "--- Deploying Frontend ---"
cd frontend || exit
npm install
npm install -g pm2
pm2 restart frontend || pm2 start "npm run dev -- --host 0.0.0.0 --port 5555" --name frontend
pm2 save
echo "Frontend deployment command issued."

echo "--- Deployment finished ---"
