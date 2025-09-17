#!/bin/bash

# 股票信息API服务启动脚本

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}股票信息API服务启动脚本${NC}"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: Python3 未安装${NC}"
    exit 1
fi

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}警告: 未检测到虚拟环境，建议使用虚拟环境${NC}"
fi

# 安装依赖
echo -e "${YELLOW}安装依赖包...${NC}"
pip install -r requirements.txt

# 设置环境变量
if [ ! -f .env ]; then
    echo -e "${YELLOW}创建环境配置文件...${NC}"
    cp .env.example .env
fi

# 启动服务
echo -e "${GREEN}启动API服务...${NC}"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo -e "${GREEN}服务已启动！${NC}"
echo "API文档地址: http://localhost:8000/docs"
echo "健康检查: http://localhost:8000/api/v1/health"
