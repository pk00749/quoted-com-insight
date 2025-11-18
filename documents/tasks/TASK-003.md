---
id: TASK-003
type: change
title: 配置化时间范围与PDF截断长度
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-001,TASK-002]
risk_level: low
---
# TASK-003 配置化时间范围与PDF截断长度

状态: ✅ 已完成
范围/模块: announcement_service / config
需求摘要:
- 过去 N 天与 PDF 截断长度参数化
实现要点:
- config.yaml: announcement_time_range_days, pdf_content_max_chars
- 环境变量优先, YAML 回退
验收:
- 修改 YAML 生效
- 环境变量覆盖成功
依赖与风险:
- 配置缺失回退默认
变更记录:
- 2025-11-17 实现读取与默认值
