## ADDED Requirements
### Requirement: WeChat Text Command Handling
系统 SHALL 通过 /wechat/callback 处理用户文本消息，支持命令与股票查询。

#### Scenario: Stock code query success
- **WHEN** 用户发送合法 6 位股票代码
- **THEN** 系统实时获取公告并返回 AI 总结（截断到安全长度）

#### Scenario: Stock code query failure
- **WHEN** 用户发送合法股票代码但获取失败
- **THEN** 系统返回友好错误提示

#### Scenario: Help command
- **WHEN** 用户发送 'help' 或 '帮助'
- **THEN** 系统返回简化的命令使用说明（仅股票查询）

#### Scenario: Invalid input
- **WHEN** 用户发送非 6 位股票代码
- **THEN** 系统返回请输入 6 位股票代码的提示
