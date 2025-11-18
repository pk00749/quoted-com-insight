---
id: TASK-002
type: change
title: AI智能总结公告API
status: done
created: 2025-11-17
updated: 2025-11-18
owners: [dev]
relates: []
dependencies: [TASK-001]
risk_level: medium
---
# TASK-002 AI智能总结公告API

状态: ✅ 已完成
范围/接口: POST /api/v1/announcements/{stock_code}/sum
需求摘要:
- 获取公告并优先解析 PDF 内容（截断）
- 对每个公告调用 LLM 生成单句摘要
- 汇总所有单句为最终 content
实现要点:
- Playwright 动态加载页面, 查找 a.pdf-link
- pdfplumber 提取文本, 清洗后截断 pdf_content_max_chars
- 回退网页正文解析
- LLM 总结（可配置/可替换）
验收:
- PDF 优先且截断生效
- 网页回退正常
- 总结字段存在且长度合理
依赖与风险:
- Playwright 浏览器安装
- PDF 内容结构异常兼容
变更记录:
- 2025-11-17 初版完成
