# 股票公告信息API服务 - 开发任务清单

## 项目概述
基于 FastAPI + AKShare 开发的股票公告信息API服务，专注于提供A股市场的公告数据查询和AI智能总结功能。

## 任务状态说明
- ✅ 已完成
- 🚧 进行中
- ❌ 待开发
- 🔄 需要重构

---

## 任务1: 获取股票公告列表API

**接口**: `GET /api/v1/announcements/{stock_code}`

### 📋 需求描述
- 获取单个股票过去10天的公告信息
- 使用 AKShare 的 `stock_notice_report` 接口
- 返回完整的公告对象列表（不获取正文内容）

### 🎯 期望功能
- 输入：股票代码（如：000001）
- 输出：公告基本信息列表（标题、类别、日期、链接等）
- 时间范围：过去10天
- 数据源：巨潮资讯网（通过AKShare）

### 📤 响应格式
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

### 💻 技术实现要点
- 移除现有的 `date` 参数，改为自动获取过去10天
- 使用 `ak.stock_notice_report(symbol='全部', date=日期)` 并按股票代码筛选
- 循环获取过去10天的数据并合并
- **仅返回公告基本信息，不获取URL正文内容**

### ⚠️ 注意事项
- 需要处理AKShare接口可能的异常
- 某些日期可能没有公告数据
- 需要去重处理相同的公告

### 📊 当前状态
✅ **已完成** - 已支持自动获取过去10天公告数据，去重处理，异常处理已实现

---

## 任务2: AI智能总结公告API

**接口**: `POST /api/v1/announcements/{stock_code}/sum`

### 📋 需求描述
- 基于股票代码获取过去10天的公告数据
- **访问每个公告的URL链接，优先通过class为pdf-link的元素获取PDF链接**
- **如获取到PDF链接，则访问该PDF文件，提取PDF正文内容并返回（仅保留前N字，N由配置项 pdf_content_max_chars 控制，默认500）**
- **如未获取到PDF链接，则回退为原有网页正文提取逻辑**
- 使用百炼大模型 Qwen3 对每个公告进行智能总结
- 将所有公告的总结再次汇总为最终的 content

### 🎯 期望功能
- 输入：股票代码
- 处理流程：
  1. 调用任务1方法获取公告列表
  2. **逐个访问每个公告的URL，解析获取正文内容**
  3. 对每个公告正文调用LLM总结成一句话
  4. 将所有单句总结再次调用LLM汇总为最终content（500字内）

### 📤 响应格式
```json
{
    "success": true,
    "data": {
        "summary": "【AI总结功能预留】针对股票：000001的公告总结",
        "content": "基于该股票过去10天的公告内容深度分析：公告1总结句+公告2总结句+...，综合分析得出最终投资观点和关键信息汇总。",
        "word_count": 485,
        "model_info": {
            "model": "qwen3",
            "provider": "百炼大模型",
            "status": "接口预留"
        }
    },
    "message": "AI总结完成（当前为预留接口）"
}
```

### 💻 技术实现要点
- 使用 Playwright 替代 BeautifulSoup 处理动态渲染的网页内容。
- 在 `_extract_announcement_content` 方法中：
  1. 使用 Playwright 加载网页。
  2. 尝试通过 `a.pdf-link` 选择器获取 PDF 链接。
  3. 如果找到 PDF 链接且以 `.pdf` 结尾，则提取 PDF 内容，并仅保留前N字（由配置项 `pdf_content_max_chars` 控制，默认500）。
  4. 如果未找到 PDF 链接，则回退到提取网页正文内容。
- 确保 Playwright 的浏览器实例在操作完成后正确关闭。

### ⚠️ 注意事项
- 确保开发环境中已安装 Playwright，并运行 `playwright install` 安装浏览器依赖。
- 处理 Playwright 的超时和异常情况，避免因网络问题导致任务失败。
- 确保提取的内容经过清理，去除多余的空格和换行符。
- 对PDF正文在清洗后进行N字截断（由配置项控制），避免空白和换行影响计数。

### 📊 当前状态
✅ **已完成** - 已实现PDF优先解析与清洗后按配置长度截断、网页正文回退、Playwright流程与资源释放，LLM总结汇总逻辑已接入（接口信息保留）。

---

## 任务3: 配置化时间范围与PDF截断长度

**目标**: 将任务1和任务2中的“过去10天”和“PDF正文前500字”设置为可配置参数

### 📋 需求描述
- 将时间范围从固定的“过去10天”改为从配置文件 `config.yaml` 中读取。
- 新增参数 `announcement_time_range_days`，用于定义时间范围（单位：天，默认10）。
- 新增参数 `pdf_content_max_chars`，用于定义PDF正文截断长度（单位：字，默认500）。

### 🎯 期望功能
- 配置文件路径：`app/core/config.yaml`
- 配置示例：
  ```yaml
  announcement_time_range_days: 10
  pdf_content_max_chars: 500
  ```
- 任务1和任务2相关逻辑需改为读取上述配置参数。

### 💻 技术实现要点
- 在 `config.yaml` 中新增 `announcement_time_range_days` 与 `pdf_content_max_chars` 参数。
- 修改 `announcement_service.py`，读取上述配置并在缺省时使用默认值（10天、500字）。
- 确保读取配置失败时有健壮的回退与日志记录。

### ⚠️ 注意事项
- 配置文件读取失败时需记录日志并使用默认值。
- 修改后的逻辑需通过单元测试验证。

### 📊 当前状态
✅ **已完成** - 已实现配置化时间范围与PDF截断长度，支持 YAML 与环境变量覆盖，默认10天与500字。

---

## 任务4: Dockerfile 检查与优化

**目标**: 确保容器环境满足本项目运行需求（FastAPI + AKShare + Playwright + pdfplumber），并具备健康检查与非 root 运行的最佳实践。

### 📋 需求描述
- 验证并完善 Dockerfile，使其在构建与运行阶段满足：
  - 安装 Playwright 及其系统依赖，并在构建阶段执行浏览器安装。
  - 支持 pdfplumber 所需依赖（如 Pillow 运行依赖）。
  - 健康检查依赖 curl 已安装可用。
  - 非 root 用户能正常运行 Playwright（浏览器文件路径可写）。
  - 时区、编码及中文字体（如需要）配置。

### 💻 技术实现要点
- 选择合适基础镜像：
  - 方案A：使用官方 Playwright 基础镜像（推荐，省去依赖安装）。
  - 方案B：在 python-slim 镜像中执行 `playwright install --with-deps` 并安装所需系统库。
- 在镜像构建阶段执行：
  - `python -m playwright install --with-deps chromium`（或全部浏览器）。
  - 安装 curl（供 HEALTHCHECK 使用）。
  - 若切换非 root 用户，确保浏览器与缓存目录（如 /ms-playwright、/home/appuser/.cache）权限正确。
- 可选优化：
  - 设置环境变量 `PLAYWRIGHT_BROWSERS_PATH` 与 `PLAYWRIGHT_DOWNLOAD_HOST`（国内源可选）。
  - 多阶段构建、缓存 pip 依赖、减少镜像体积。

### ✅ 检查清单
- [ ] 镜像可构建成功，且运行时 uvicorn 正常启动。
- [ ] GET /api/v1/announcements/{code} 可返回数据。
- [ ] POST /api/v1/announcements/{code}/sum 可执行（Playwright 能打开页面并提取 PDF/正文）。
- [ ] HEALTHCHECK 正常（curl 可用）。
- [ ] 非 root 用户运行无权限问题（Playwright 浏览器可启动）。
- [ ] 中国大陆网络环境下具备可选加速配置（如 apt 源、Playwright 下载源）。

### ⚠️ 注意事项
- 若使用 python:slim 系列，需安装 Playwright 依赖（如 libnss3、libgbm、libgtk-3-0、libdrm、libasound2 等）。
- pdfplumber 依赖 Pillow，可能需要系统库（zlib、libjpeg 等）。
- 若需要渲染中文或处理特殊 PDF，建议安装中文字体包（如 `fonts-noto-cjk`）。

### 📊 当前状态
❌ **待开发** - 需要审阅现有 Dockerfile 并补充依赖与安装步骤，完成验证与测试。
