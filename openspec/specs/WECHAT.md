## ADDED Requirements
### Requirement: WeChat Text Command Handling
系统 SHALL 通过 /wechat/callback 处理用户文本消息，支持命令与股票查询。

#### Scenario: Stock code query success
- **WHEN** 用户发送合法 6 位股票代码
- **THEN** 若有缓存则返回缓存，否则生成总结并截断到安全长度

#### Scenario: Help command
- **WHEN** 用户发送 'help' 或 '帮助'
- **THEN** 系统返回命令使用说明

### Requirement: Subscribe Command
系统 SHALL 在用户发送 'subscribe'|'list'|'my' 时返回其订阅的股票代码（排序，>100 截断）。

#### Scenario: Empty subscription
- **WHEN** 用户没有任何订阅代码
- **THEN** 系统返回引导用户添加代码的提示

#### Scenario: Non-empty subscription
- **WHEN** 用户存在订阅
- **THEN** 系统返回升序列表并在超过 100 时提示截断

### Requirement: Add Subscription Command
系统 SHALL 在匹配 ^add\d{6}$ 的命令时新增 6 位股票代码订阅。

#### Scenario: Add new code
- **WHEN** 代码尚未订阅
- **THEN** 系统存储并确认

#### Scenario: Add duplicate
- **WHEN** 代码已存在订阅列表
- **THEN** 系统提示已存在

### Requirement: Delete Subscription Command
系统 SHALL 在匹配 ^del\d{6}$ 的命令时删除 6 位股票代码订阅。

#### Scenario: Remove existing code
- **WHEN** 代码存在
- **THEN** 系统删除并确认

#### Scenario: Remove non-existing code
- **WHEN** 代码不存在
- **THEN** 系统提示不存在

### Requirement: Subscribe Timestamp Display (Planned)
系统 SHALL 在订阅列表输出中展示每个订阅代码对应的最近 summary 时间戳。

#### Scenario: No timestamp
- **WHEN** 代码从未生成过总结
- **THEN** 显示 '尚未刷新'

## MODIFIED Requirements
### Requirement: Daily Scheduled Summary Generation
系统 SHALL 使用配置的 subscription_refresh_time 调度每日汇总任务以替换硬编码 09:00。

#### Scenario: Post-time scheduling
- **WHEN** 当前时间已超过配置的 HH:MM
- **THEN** 安排在下一天相同 HH:MM 运行

## ADDED Requirements
### Requirement: Refresh Command (Planned)
系统 SHALL 支持使用 ^refresh\d{6}$ 模式的命令即时重新生成总结并复用现有流程。

#### Scenario: Immediate refresh success
- **WHEN** 用户发送 refresh+代码且生成成功
- **THEN** 缓存 JSON 与时间戳更新并返回结果

#### Scenario: Refresh failure
- **WHEN** 生成失败
- **THEN** 系统返回友好错误提示
