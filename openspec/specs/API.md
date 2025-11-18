## ADDED Requirements
### Requirement: Announcement Listing API
系统 SHALL 提供 GET /api/v1/announcements/{stock_code} 接口返回过去 N 天过滤后的公告列表。

#### Scenario: Successful retrieval
- **WHEN** 客户端使用合法 6 位股票代码请求
- **THEN** 系统返回 success=true 与公告列表（不包含公告正文内容）

### Requirement: Announcement Summary API
系统 SHALL 提供 POST /api/v1/announcements/{stock_code}/sum 接口返回 AI 汇总内容。

#### Scenario: PDF first strategy
- **WHEN** 系统检测到指向 .pdf 的 pdf-link 元素
- **THEN** 优先抽取 PDF 文本（按 pdf_content_max_chars 截断）然后才回退到 HTML 正文

## MODIFIED Requirements
### Requirement: Configurable Time Range
系统 SHALL 从 config.yaml 读取 announcement_time_range_days 决定过去 N 天窗口。

#### Scenario: Fallback default
- **WHEN** 配置缺失或非法
- **THEN** 使用默认值 10

## ADDED Requirements
### Requirement: Subscription Refresh Time Configuration
系统 SHALL 读取 subscription_refresh_time (HH:MM Asia/Shanghai) 以调度每天的汇总任务。

#### Scenario: Next-day scheduling
- **WHEN** 当前时间已超过当日配置的 HH:MM
- **THEN** 计划在下一天相同 HH:MM 执行
