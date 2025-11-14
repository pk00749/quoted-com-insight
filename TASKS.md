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
  - 配置国内 APT 源以加速依赖安装。

### 💻 技术实现要点
- 选择合适基础镜像：
  - 方案A：使用官方 Playwright 基础镜像（推荐，省去依赖安装）。
  - 方案B：在 python-slim 镜像中执行 `playwright install --with-deps` 并安装所需系统库。
- 在镜像构建阶段执行：
  - `python -m playwright install --with-deps chromium`（或全部浏览器）。
  - 安装 curl（供 HEALTHCHECK 使用）。
  - 若切换非 root 用户，确保浏览器与缓存目录（如 /ms-playwright、/home/appuser/.cache）权限正确。
  - 配置国内 APT 源以加速依赖安装。
- 可选优化：
  - 使用虚拟环境（venv）隔离 Python 依赖，避免系统级安装限制。
  - 清理构建缓存，减小镜像体积。

### ✅ 状态
- 已完成

---

## 任务5: API 与微信公众号对接（文档与步骤）

**目标**: 用户在微信公众号与客服聊天窗口输入证券代码（如“000001”），系统返回该股票近N天公告总结（调用任务2接口）。

### 🧭 架构与交互流程
1) 用户在公众号发送文本消息（证券代码）
2) 微信服务器将消息推送至业务服务的回调URL（POST）
3) 回调服务验签、解析文本，识别股票代码
4) 调用内部API：POST /api/v1/announcements/{stock_code}/sum 获取总结
5) 将总结组织为公众号文本消息，回复给用户

### 🪜 接入步骤（运营与配置）
1. 公众号准备
   - 账号类型：建议服务号（或使用“公众平台测试号”进行联调）
   - 获取 AppID、AppSecret
   - 配置服务器配置（开发设置）：
     - URL：例如 https://your-domain/wechat/callback
     - Token：自定义字符串，用于签名校验
     - EncodingAESKey：平台生成，用于消息加解密
     - 消息加解密方式：建议“兼容模式”或“安全模式”
2. 域名与网络
   - 提供公网可访问的 HTTPS 域名，证书有效
   - 可选：在网关/反向代理处做限流与白名单
3. 回调URL联调（仅流程说明，不写代码）
   - GET /wechat/callback：微信服务器用于“接入校验”
     - 校验参数：signature、timestamp、nonce、echostr
     - 服务端按规则对 token、timestamp、nonce 做 SHA1，匹配 signature，通过后原样返回 echostr
   - POST /wechat/callback：接收用户消息
     - 按公众号配置的加密模式解析 XML 消消息体，提取 MsgType=text、Content
     - 业务处理后返回被动回复 XML（或使用客服消息接口主动推送）

### 🔤 消息与解析规范（文本）
- 股票代码识别：
  - 支持 6 位数字（如 000001）
  - 可扩展支持带交易所前缀（如 SZ000001/SH600000），内部统一到 6 位代码
- 非法输入处理：返回引导提示，例如“请发送6位A股代码，如 000001”

### 🔗 API映射（内部调用）
- 汇总接口：POST /api/v1/announcements/{stock_code}/sum
- 成功响应关键字段：content（最终汇总文本）、word_count
- 超长文本分段：公众号单条文本上限约2k~4k字符，超过需拆分多条回复

### 🧱 安全与合规
- 必须进行签名校验（signature）与重放防护（timestamp/nonce）
- 安全/兼容模式下进行 AES 解密与加密回复
- 幂等：依据 FromUserName + MsgId 或 CreateTime 做去重处理，避免重复调用
- 隐私与合规：不存储用户敏感数据，仅记录必要审计日志

### 🚦 频控与缓存建议
- 频控：对同一用户/同一股票在短时间内限流（如 60s 内最多1次）
- 缓存：
  - 对 sum 结果做短时缓存（如 10~30 分钟），命中则直接返回
  - 失败重试与降级：返回“当前服务繁忙，请稍后重试”

### 🚀 部署与运维
- 服务需要：
  - 暴露 /wechat/callback（80/443）
  - 内部可访问本项目 API（同一容器或同一网络均可）
- 日志与监控：
  - 记录验签失败、解析失败、调用内部API超时等关键事件
  - 指标：成功率、平均延迟、超时率、调用配额（LLM/Playwright）

### 🧪 验收清单
- [x] 服务器配置校验通过（GET 验签成功）
- [x] 文本消息“000001”可返回总结
- [ ] 异常输入有正确的引导文案
- [ ] 超长内容会智能分段
- [ ] 限流与缓存策略生效
- [ ] 安全模式收发消息加解密正确

### 📊 当前状态
✅ **已完成** - 文档与联调完成，回调流程已验证可用。

---

## 任务6: 使用 Docker Compose 部署 Nginx 与应用服务（仅文档，先不实现代码）

**目标**: 通过 docker compose 同时部署反向代理（Nginx，支持 SSL）与本服务容器，提供对外 HTTPS 访问与到应用的反向代理。

### 📁 文件与目录规划（预留）
- `docker-compose.yml`（或 `compose.yaml`）：定义 nginx 与 app 两个服务
- `deploy/nginx/nginx.conf`：Nginx 主配置（含 HTTPS 与反向代理）
- `certs/`：存放 SSL 证书与私钥（预留，不随仓库提交）
  - `fullchain.pem`（或 `server.crt`）
  - `privkey.pem`（或 `server.key`）

### 🧩 Compose 设计（预案）
- 网络：单一自定义网络 `webnet`，nginx 与 app 互通
- 服务：
  - app：
    - 基于当前项目 Dockerfile 构建或使用已发布镜像
    - 暴露 8000 端口（仅容器内可见），健康检查指向 `/health`
  - nginx：
    - 依赖 app 启动，映射主机 80、443 端口
    - 只读挂载 `deploy/nginx/nginx.conf -> /etc/nginx/nginx.conf`
    - 只读挂载 `certs -> /etc/nginx/certs`（证书目录，预留）

### ⚙️ Nginx 配置要点（nginx.conf 预留规范）
- upstream `app` 指向 `app:8000`
- HTTP 80：全量 301 跳转到 HTTPS
- HTTPS 443：
  - `ssl_certificate /etc/nginx/certs/fullchain.pem;`
  - `ssl_certificate_key /etc/nginx/certs/privkey.pem;`
  - 开启 `http2`、合理的 `ssl_protocols` 与 `ssl_ciphers`
  - 反向代理到 `http://app`，传递头部：`Host`、`X-Forwarded-For`、`X-Forwarded-Proto`
  - WebSocket 支持：`Upgrade` 与 `Connection` 头

### 🧪 验收清单
- [x] `docker compose up -d` 后两个容器均为 healthy
- [x] 访问 `http://` 自动跳转 `https://`
- [ ] 证书挂载后 HTTPS 正常握手
- [x] `https://<domain>/health` 经 Nginx 反代可达 app 健康检查

### 📊 当前状态
✅ **已完成** - 已提交 docker-compose.yml 与 deploy/nginx/nginx.conf，证书与微信直通路径已配置（详见下方“任务6（更新）”）。

---

## 任务7: 微信订阅与定时刷新（仅文档，先不实现代码）

### 📋 需求描述
1. wechat.py 增加一个 add 指令，用于每次只把一个股票代码加入定时刷新的列表。例子：add600000。
2. wechat.py 增加一个 del 指令，用于每次只把一个股票代码从定时刷新的列表中删除。例子：del600000。
3. 基于 SQLite 存储定时刷新列表，创建一个表：
   - 字段1：from_user
   - 字段2：stock_code_list（例如 {"600000", "600001"}）
   - 字段3：updated_datetime（当前数据更新时间）
4. 设置一个定时逻辑：每天北京时间早上 9 点，遍历表的字段 stock_code_list 里的股票代码，调用 announcement_service.summarize_announcements 进行总结；总结后的结果以股票代码为文件名保存为 JSON 格式，如 600000.json。
5. 当用户输入股票代码后，返回对应 JSON 文件里的内容。

### 🧪 验收清单
- [x] add 指令能将 6 位股票代码加入订阅列表
- [x] del 指令能将 6 位股票代码从订阅列表移除
- [x] 09:00 定时任务按期运行并生成对应 JSON 文件（后台协程实现）
- [x] 用户发送 6 位股票代码时能返回 JSON 内容（命中缓存或实时生成并落盘）

### 📊 当前状态
✅ 已完成（实现订阅指令、SQLite存储、缓存JSON及定时09:00生成逻辑）
