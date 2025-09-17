# 股票公告信息API服务

基于FastAPI + akshare构建的股票公告信息API服务，专为n8n工作流优化，支持百炼大模型智能总结。

## 📋 项目概述

专注于股票公告信息获取和处理的API服务，提供实时数据获取、智能总结和n8n集成功能。

## ✨ 核心特性

- 🚀 **高性能异步**: 基于FastAPI的异步API架构
- 📊 **实时数据**: 集成akshare库获取实时股票公告数据
- 🤖 **AI总结**: 支持百炼qwen3智能总结（预留接口，500字限制）
- 🔗 **n8n集成**: 优化的Webhook接口，完美适配n8n工作流
- 📈 **日级数据**: 支持日期范围查询，无需本地存储
- 🎯 **单股查询**: 支持单个股票代码查询
- 🔧 **结构化输出**: 要点提取 + 影响分析

## 🛠️ 技术栈

- **后端框架**: FastAPI
- **数据源**: akshare
- **AI模型**: 百炼大模型qwen3（预留）
- **容器化**: Docker
- **测试**: pytest

## 📚 API接口文档

### 核心接口

#### 1. 获取股票公告列表
```http
GET /api/v1/announcements/{stock_code}
```

**参数**：
- `stock_code`: 股票代码（支持多种格式：000001、000001.SZ等）
- `start_date`: 开始日期 YYYY-MM-DD（可选，默认最近30天）
- `end_date`: 结束日期 YYYY-MM-DD（可选，默认今天）
- `page`: 页码（可选，默认1）
- `size`: 每页大小（可选，默认20，最大100）

**响应示例**：
```json
{
    "success": true,
    "data": {
        "announcements": [
            {
                "id": "000001_001",
                "stock_code": "000001",
                "stock_name": "平安银行",
                "title": "关于董事会决议的公告",
                "publish_date": "2025-09-17",
                "category": "董事会决议",
                "url": "https://...",
                "content": "公告摘要...",
                "importance": "high",
                "keywords": ["董事会", "决议"]
            }
        ],
        "total": 15,
        "page": 1,
        "size": 20
    },
    "message": "获取公告成功"
}
```

#### 2. 获取最新公告
```http
GET /api/v1/announcements/latest
```

**参数**：
- `date`: 指定日期 YYYY-MM-DD（可选，默认今天）
- `limit`: 返回数量限制（可选，默认50，最大200）
- `category`: 公告类别筛选（可选）

#### 3. AI智能总结公告
```http
POST /api/v1/announcements/summarize
```

**请求体**：
```json
{
    "announcement": {
        "title": "公告标题",
        "content": "公告内容",
        "stock_code": "000001"
    }
}
```

**响应示例**：
```json
{
    "success": true,
    "data": {
        "summary": "AI总结内容（500字内）",
        "key_points": [
            "• 关键要点1",
            "• 关键要点2",
            "• 关键要点3"
        ],
        "impact_analysis": {
            "positive_impact": "正面影响分析",
            "negative_impact": "负面影响分析",
            "neutral_impact": "中性影响分析"
        },
        "investment_suggestion": "投资建议",
        "word_count": 456,
        "model_info": {
            "model": "qwen3",
            "provider": "百炼大模型",
            "status": "接口预留"
        }
    },
    "message": "AI总结完成"
}
```

#### 4. n8n专用Webhook接口
```http
POST /api/v1/webhook/announcements
```

**请求体**：
```json
{
    "stock_codes": ["000001", "000002"],
    "date": "2025-09-17"
}
```

#### 5. 健康检查（n8n专用）
```http
GET /api/v1/health
```

## 🚀 快速开始

### 本地开发

1. **克隆项目**：
```bash
git clone <repository-url>
cd quoted-com-insight
```

2. **安装依赖**：
```bash
pip install -r requirements.txt
```

3. **启动服务**：
```bash
python -m app.main
```

4. **访问文档**：
- API文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc

### Docker部署

```bash
# 构建镜像
docker build -t stock-announcement-api .

# 运行容器
docker run -p 8000:8000 stock-announcement-api
```

### Docker Compose

```bash
docker-compose up -d
```

## 🔗 n8n集成指南

### 1. 健康检查节点
```
GET http://your-api-host:8000/api/v1/health
```

### 2. 获取股票公告
```
GET http://your-api-host:8000/api/v1/announcements/000001?start_date=2025-09-01&end_date=2025-09-17
```

### 3. Webhook批量处理
```
POST http://your-api-host:8000/api/v1/webhook/announcements
Content-Type: application/json

{
    "stock_codes": ["000001", "000002", "600036"],
    "date": "2025-09-17"
}
```

## 📊 数据特性

- **实时性**: 直接从akshare获取最新数据，无本地缓存
- **准确性**: 基于权威数据源的公告信息
- **完整性**: 包含公告标题、内容、分类、链接等完整信息
- **智能化**: AI自动判断公告重要性和提取关键词

## 🔧 配置说明

主要配置在 `app/core/config.py` 中：

```python
class Settings:
    app_name: str = "股票公告信息API服务"
    version: str = "1.0.0"
    # 其他配置...
```

## 🧪 测试

```bash
# 运行测试
pytest

# 运行特定测试
pytest tests/test_quoted_com_insight_api.py -v
```

## 📈 扩展规划

- ✅ **第一阶段**: 公告信息服务（已完成）
- 🔄 **第二阶段**: 百炼大模型集成
- 📋 **后续阶段**: 扩展其他股票信息类型

## ⚠️ 注意事项

1. **数据依赖**: 服务依赖akshare库和相关数据源的可用性
2. **请求频率**: 建议控制请求频率，避免对数据源造成压力
3. **错误处理**: 服务包含完善的错误处理和重试机制
4. **AI功能**: 当前AI总结为预留接口，待后续集成

## 📝 更新日志

### v1.0.0 (2025-09-17)
- ✅ 完成基础架构搭建
- ✅ 集成akshare数据源
- ✅ 实现公告列表获取
- ✅ 添加n8n专用接口
- ✅ 预留AI总结接口
- ✅ 完善错误处理和日志

## 📞 支持

如有问题或建议，请提交Issue或联系开发团队。
