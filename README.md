# 股票公告信息API服务

基于 FastAPI + AKShare 开发的股票公告信息API服务，专注于提供A股市场的公告数据查询和AI智能总结功能。

## 🚀 功能特性

- **公告数据获取**：使用 AKShare 的 `stock_notice_report` 接口获取股票公告
- **日级数据**：支持查询指定日期的股票公告信息
- **实时获取**：无持久化存储，每次请求实时获取最新数据
- **AI智能总结**：集成百炼大模型 Qwen3 进行公告智能总结（预留接口）
- **Webhook支持**：为 n8n 工作流优化的 Webhook 接口
- **RESTful API**：标准的 REST 风格接口设计

## 🛠️ 技术栈

- **框架**：FastAPI
- **数据源**：AKShare
- **AI模型**：百炼大模型 Qwen3（预留）
- **语言**：Python 3.8+

## 📦 安装与运行

### 环境要求
- Python 3.8+
- pip

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用启动脚本
bash start.sh
```

### Docker 部署
```bash
# 构建镜像
docker build -t stock-announcement-api .

# 运行容器
docker run -p 8000:8000 stock-announcement-api

# 或使用 docker-compose
docker-compose up -d
```

## 📚 API接口文档

### 核心接口

#### 1. 获取股票公告列表
```http
GET /api/v1/announcements/{stock_code}
```

**参数**：
- `stock_code`: 股票代码（必填）

**说明**：
- 使用 AKShare 的 `stock_notice_report` 接口获取数据
- 数据来源：各大证券交易所官方公告
- 自动获取过去10天的公告信息
- 返回公告详情链接列表

**响应示例**：
```json
{
    "success": true,
    "data": {
        "announcements": [
            {
                "stock_code": "000001",
                "stock_name": "平安银行",
                "title": "关于召开2024年第三次临时股东大会的通知",
                "category": "临时股东大会",
                "publish_date": "2024-09-17",
                "url": "http://static.cninfo.com.cn/finalpage/..."
            }
        ],
        "total": 1,
        "page": 1,
        "size": 20
    },
    "message": "获取公告成功"
}
```

#### 2. AI智能总结公告
```http
POST /api/v1/announcements/summarize
```

**请求体**：
```json
{
    "stock_code": "000001"
}
```

**说明**：
- 基于 `/api/v1/announcements/{stock_code}` 获取公告数据
- 使用百炼大模型 Qwen3 进行智能总结（预留接口）
- 自动获取该股票过去10天的公告并进行总结
- 总结字数限制在500字内

**响应示例**：
```json
{
    "success": true,
    "data": {
        "summary": "【AI总结功能预留】针对股票：000001的公告总结",
        "content": "基于该股票过去10天的公告内容，通过百炼大模型Qwen3分析得出：该公司近期发布了多项重要公告，包括业务发展、财务状况等关键信息。具体分析内容将在AI模型集成后提供详细的结构化总结。（当前为预留接口，500字内）",
        "word_count": 0,
        "model_info": {
            "model": "qwen3",
            "provider": "百炼大模型",
            "status": "接口预留"
        }
    },
    "message": "AI总结完成（当前为预留接口）"
}
```

#### 3. Webhook接口（n8n专用）
```http
POST /api/v1/webhook/announcements
```

**请求体**：
```json
{
    "stock_codes": ["000001", "000002"],
    "date": "2024-09-17"
}
```

**响应示例**：
```json
{
    "success": true,
    "data": [
        {
            "stock_code": "000001",
            "announcements": {
                "announcements": [...],
                "total": 5,
                "page": 1,
                "size": 50
            }
        }
    ],
    "message": "Webhook处理成功，共处理2只股票"
}
```

### 系统接口

#### 健康检查
```http
GET /health
```

#### 系统信息
```http
GET /api/v1/system/info
```

## 🔧 配置说明

### 环境变量
创建 `.env` 文件：
```env
# 服务配置
APP_NAME=股票公告API服务
APP_VERSION=1.0.0
DEBUG=true

# API配置
API_V1_STR=/api/v1

# 日志配置
LOG_LEVEL=INFO
```

## 📖 数据源说明

### AKShare stock_notice_report 接口

本服务使用 AKShare 的 `stock_notice_report` 接口获取股票公告数据：

- **接口名称**：`ak.stock_notice_report(symbol="财务报告", date="20240917")`
- **数据来源**：巨潮资讯网
- **更新频率**：实时更新
- **数据覆盖**：沪深A股市场

**返回字段说明**：
- `代码`: 股票代码
- `名称`: 股票简称
- `公告标题`: 公告标题
- `公告类型`: 公告分类
- `公告日期`: 发布日期
- `网址`: 公告详情链接

## 🔄 使用场景

1. **财经媒体**：自动获取和分析股票公告
2. **量化投资**：公告数据驱动的投资策略
3. **风险监控**：重要公告的实时监控
4. **数据分析**：股票公告的统计分析
5. **工作流自动化**：结合 n8n 构建自动化数据处理流程

## 🤝 开发指南

### 项目结构
```
quoted-com-insight/
├── app/
│   ├── core/           # 核心配置和异常处理
│   ├── models.py       # 数据模型定义
│   ├── routers/        # API路由
│   ├── services/       # 业务逻辑服务
│   └── main.py         # 应用入口
├── tests/              # 测试文件
├── requirements.txt    # 依赖包
├── Dockerfile         # Docker配置
└── README.md          # 项目文档
```

### 本地开发

1. 克隆项目：
```bash
git clone <repository-url>
cd quoted-com-insight
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 启动开发服务器：
```bash
uvicorn app.main:app --reload
```

5. 访问 API 文档：
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 测试
```bash
# 运行测试
pytest

# 运行特定测试
pytest tests/test_akshare_api.py
```

## 📝 更新日志

### v1.0.0 (2024-09-17)
- 初始版本发布
- 支持股票公告数据获取
- 集成 AKShare stock_notice_report 接口
- 提供 Webhook 接口支持 n8n
- 预留 AI 智能总结功能

## 🔗 相关链接

- [AKShare 文档](https://akshare.akfamily.xyz/)
- [FastAPI 官网](https://fastapi.tiangolo.com/)
- [百炼大模型](https://bailian.aliyun.com/)

## 📄 许可证

MIT License

## 🙋‍♂️ 联系我们

如有问题或建议，请提交 Issue 或 Pull Request。
