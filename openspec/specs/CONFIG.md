## ADDED Requirements
### Requirement: Configurable Announcement Time Range
系统 SHALL 使用 `announcement_time_range_days`（来自 YAML 或环境变量）确定公告与汇总的过去 N 天窗口。

#### Scenario: Missing key
- **WHEN** YAML 与环境变量都缺失该键
- **THEN** 默认使用 10

### Requirement: Configurable PDF Content Truncation
系统 SHALL 使用 `pdf_content_max_chars` 在清洗后截断抽取的 PDF 文本。

#### Scenario: Oversized PDF
- **WHEN** PDF 文本长度超过配置限制
- **THEN** 仅返回前面截断长度的内容

### Requirement: Configurable Daily Subscription Refresh Time
系统 SHALL 依据 `subscription_refresh_time` (HH:MM Asia/Shanghai) 调度每日订阅汇总。

#### Scenario: Invalid format
- **WHEN** 值不符合 HH:MM 模式或超出范围
- **THEN** 记录警告并回退为默认 09:00

### Requirement: Environment Override Precedence
系统 SHALL 允许环境变量覆盖 YAML 配置值（环境优先）。

#### Scenario: Env override present
- **WHEN** 设置了 ANNOUNCEMENT_TIME_RANGE_DAYS 环境变量
- **THEN** 使用其值而忽略 YAML 中对应项

## MODIFIED Requirements
### Requirement: WeChat Token Retrieval
系统 SHALL 在启动时从环境获取 `WECHAT_TOKEN`；若缺失则回调验签失败返回 403。

#### Scenario: Token missing
- **WHEN** 环境未设置 WECHAT_TOKEN
- **THEN** 验签计算失败并返回 403
