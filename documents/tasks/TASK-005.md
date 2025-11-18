---
id: TASK-005
type: change
title: 微信公众号对接
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-001,TASK-002]
risk_level: medium
---
# TASK-005 微信公众号对接
状态: ✅ 已完成
范围/接口: /wechat/callback (GET/POST)
需求摘要:
- 验签回调, 输入代码返回公告智能总结
实现要点:
- GET 验签: signature 校验
- POST 明文 XML 解析 -> 股票代码识别 -> 调用 summarize
- 分段返回(长度控制)
验收:
- 验签通过返回 echostr
- 输入6位代码返回总结文本
依赖与风险:
- 微信服务器访问 HTTPS
变更记录:
- 2025-11-17 联调通过
