---
id: TASK-014
type: change
title: refresh 命令即时刷新
status: proposed
created: 2025-11-18
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-007]
risk_level: low
---
# TASK-014 refresh 命令即时刷新
状态: ❌ 待开发
范围: wechat 命令(刷新) + 定时逻辑复用

需求摘要:
- 新增输入命令 refresh，形如 `refresh600000`
- 对指定 6 位股票代码进行“立即刷新”，生成与定时任务一致的 JSON 总结结果
- 即时刷新应复用定时刷新的同一实现逻辑，保证两者输出一致，仅触发时机不同

实现要点(规划):
- wechat 文本解析: `^refresh(\d{6})$`
- 复用定时任务的生成流程：announcement_service.summarize_announcements -> subscription_service.save_summary
- 刷新完成后可直接返回最新内容（与查询代码行为一致）
- 异常处理：网络/抓取失败返回友好提示，不影响后续定时任务
- 频控建议：对同一用户同一股票短时内限流(如 60s)

验收(规划):
- 发送 `refresh600000` 后能触发生成 JSON，并返回新结果
- 与定时产出的结果字段一致（content/summary）且覆盖旧文件
- 若代码非法或服务不可用，返回清晰错误提示

依赖与风险:
- announcement_service 可用性与 Playwright/PDF 依赖
- 与现有缓存/订阅时间戳的并发写入

变更记录:
- 2025-11-18 创建任务文档（规划）
