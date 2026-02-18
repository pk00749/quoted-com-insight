## 1. Implementation

- [x] 1.1 简化 `app/routers/wechat.py` - 移除 subscribe/add/del/refresh 命令处理逻辑
- [x] 1.2 简化帮助文本，只保留股票代码查询说明
- [x] 1.3 删除 `app/services/subscription_service.py`
- [x] 1.4 删除 `app/routers/commands/subscribe.py`
- [x] 1.5 删除 `app/routers/commands/add.py`
- [x] 1.6 删除 `app/routers/commands/delete.py`
- [x] 1.7 更新 `app/routers/commands/__init__.py` - 移除相关导入
- [x] 1.8 删除 `app/routers/commands/utils.py` - 移除订阅相关辅助函数
- [x] 1.9 更新 `app/routers/commands/query.py` - 移除缓存，直接调用公告服务
- [x] 1.10 更新 `app/main.py` - 移除定时任务和 subscription_service 导入

## 2. Testing

- [x] 2.1 更新 test_wechat_commands.py - 删除订阅相关测试，添加查询测试
- [x] 2.2 删除 test_wechat_refresh_command.py - refresh 命令已移除

## 3. Documentation

- [x] 3.1 更新 openspec/specs/WECHAT.md - 移除订阅相关需求
- [x] 3.2 更新 openspec/specs/CONFIG.md - 移除订阅刷新时间配置
- [x] 3.3 更新 openspec/specs/logging/spec.md - 更新日志场景

## 4. Rollback Plan

- [ ] 4.1 如需回滚，从 git 恢复删除的文件和修改的代码
