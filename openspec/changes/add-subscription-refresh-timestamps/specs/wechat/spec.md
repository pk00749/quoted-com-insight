## MODIFIED Requirements
### Requirement: Subscribe Timestamp Display (Planned)
System SHALL show last summary timestamp for each subscribed code in subscribe output.

#### Scenario: Timestamp exists
- **WHEN** code has summary file
- **THEN** show converted Asia/Shanghai time 'YYYY-MM-DD HH:MM'

#### Scenario: No timestamp
- **WHEN** code never summarized
- **THEN** show '尚未刷新'
## 1. Implementation
- [ ] 1.1 读取 subscription_refresh_time 配置并校验
- [ ] 1.2 定时计算下一触发秒数逻辑实现
- [ ] 1.3 在订阅输出中加入更新时间戳查询
- [ ] 1.4 添加格式化函数(UTC -> Asia/Shanghai)
- [ ] 1.5 增加单测: 配置生效、非法格式回退、时间戳展示
- [ ] 1.6 更新文档与 WECHAT/CONFIG 规格状态

## 2. Testing
- [ ] 用例: 合法 HH:MM
- [ ] 用例: 非法值回退
- [ ] 用例: 未刷新显示"尚未刷新"

## 3. Rollback
- [ ] 移除解析与展示逻辑
- [ ] 删除新增的时间戳字段显示

