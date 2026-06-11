#!/bin/bash
# ======================================
# 部署脚本：浙江大学化学系学生会工作站
# 用法：在服务器上执行：bash deploy.sh
# ======================================
set -e

echo "=== 浙江大学化学系学生会工作站 部署脚本 ==="

# --- 配置 ---
APP_DIR="/var/www/zjuchem"
DATA_DIR="/var/data/zjuchem"
PYTHON="/usr/bin/python3"
SERVICE_NAME="zjuchem-backend"

# --- 1. 创建目录 ---
echo "[1/7] 创建目录结构..."
sudo mkdir -p $APP_DIR/backend $APP_DIR/frontend $DATA_DIR/uploads
sudo chown -R www-data:www-data $APP_DIR $DATA_DIR

# --- 2. 部署后端 ---
echo "[2/7] 部署后端代码..."
sudo cp -r backend/app backend/requirements.txt $APP_DIR/backend/

# --- 3. 创建 Python 虚拟环境 ---
echo "[3/7] 创建 Python 虚拟环境..."
$PYTHON -m venv $APP_DIR/backend/venv
source $APP_DIR/backend/venv/bin/activate
pip install --upgrade pip
pip install -r $APP_DIR/backend/requirements.txt

# --- 4. 初始化数据库 ---
echo "[4/7] 初始化 SQLite 数据库..."
sudo -u www-data mkdir -p $DATA_DIR
cd $APP_DIR/backend
sudo -u www-data $APP_DIR/backend/venv/bin/python deploy/init_db.py

# --- 5. 构建前端 ---
echo "[5/7] 构建前端..."
cd /tmp  # 临时，实际前端在本地构建好后上传更简单
echo "   前端请在本机构建后 scp dist/ 到 $APP_DIR/frontend/"
echo "   cd frontend && npm run build && scp -r dist/* user@124.220.64.29:$APP_DIR/frontend/"

# --- 6. 安装 systemd 服务 ---
echo "[6/7] 安装 systemd 服务..."
sudo cp deploy/zjuchem-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

# --- 7. Nginx 配置 ---
echo "[7/7] 配置 Nginx..."
sudo cp deploy/nginx-zjuchem.conf /etc/nginx/sites-available/zjuchem
sudo ln -sf /etc/nginx/sites-available/zjuchem /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "=== 部署完成！==="
echo "前端: https://zjuchem.top"
echo "API:  https://zjuchem.top/api/health"
echo "后端状态: sudo systemctl status $SERVICE_NAME"
echo "后端日志: sudo journalctl -u $SERVICE_NAME -f"
