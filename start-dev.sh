#!/bin/bash
# 本地开发快速启动
# 先启动后端，再启动前端

echo "Starting backend..."
cd backend
python3 -m venv venv 2>/dev/null
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
pip install -q -r requirements.txt
python deploy/init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting frontend..."
cd ../frontend
npm install --silent
npm run dev &
FRONTEND_PID=$!

echo ""
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8000"
echo "按 Ctrl+C 停止"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
