## 1. Implementation
- [x] 1.1 解析 refresh 命令正则（^refresh\d{6}$ 已在 wechat.py 实现）
- [x] 1.2 复用 summarize 流程生成 JSON（调用 announcement_service.summarize_announcements + save_summary）
- [x] 1.3 写入更新时间戳（save_summary 内持久记录 summary_updated_datetime）
- [x] 1.4 频控逻辑实现(简单内存字典)（同一代码 60s 间隔）
- [x] 1.5 单测: 成功刷新/频控触发（tests/test_wechat_refresh_command.py）
- [x] 1.6 更新 WECHAT 规格状态（已在 specs/wechat/spec.md 增加返回格式描述）

## 2. Rollback
- [ ] 移除命令解析与处理分支

