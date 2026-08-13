#!/bin/bash
# 英语 70 天学习系统 - 本地部署脚本
# 使用 OrbStack Docker 进行部署

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="english-learning-app"
PORT=3000

echo "=============================="
echo " 英语 70 天学习系统 - 部署"
echo "=============================="
echo ""

# 检查 Docker 是否可用
if ! command -v docker &> /dev/null; then
    echo "❌ 未找到 Docker，请先启动 OrbStack"
    exit 1
fi

echo "✅ Docker 已就绪"

# 停止并删除旧容器（如果存在）
if docker ps -a --format '{{.Names}}' | grep -q "^${APP_NAME}$"; then
    echo "🔄 停止旧容器..."
    docker stop "$APP_NAME" 2>/dev/null || true
    docker rm "$APP_NAME" 2>/dev/null || true
fi

# 构建镜像
echo "🔨 构建镜像..."
docker build -t "$APP_NAME" .

# 运行容器
echo "🚀 启动容器..."
docker run -d \
    --name "$APP_NAME" \
    -p "${PORT}:80" \
    --restart unless-stopped \
    "$APP_NAME"

echo ""
echo "=============================="
echo " ✅ 部署完成！"
echo "=============================="
echo ""
echo "访问地址: http://localhost:${PORT}"
echo ""
echo "常用命令:"
echo "  查看日志:  docker logs -f ${APP_NAME}"
echo "  停止服务:  docker stop ${APP_NAME}"
echo "  启动服务:  docker start ${APP_NAME}"
echo "  删除服务:  docker rm -f ${APP_NAME}"
echo ""
