## 1. Implementation
- [x] 1.1 Add logging configuration (console + rotating file) honoring LOG_LEVEL and defaulting path to /opt/quoted-com-insight/logs/app.log
- [x] 1.2 Ensure container startup creates log directory and writes a startup entry accessible from host when path is mounted
- [x] 1.3 Instrument announcements flow: fetch window, counts, success/failure, summarize start/end, per-code errors
- [x] 1.4 Instrument WeChat command handling with sanitized user/command info and error traces
- [x] 1.5 Instrument system/health endpoints and scheduler lifecycle (start/stop/next-run)
- [x] 1.6 Update config doc entries for log level/path

## 2. Validation
- [x] 2.1 Local run: verify app.log created under /opt/quoted-com-insight/logs with rotated chunks and contains startup + sample API calls
- [x] 2.2 Container run: with volume mount to /opt/quoted-com-insight/logs, tail logs from host and confirm entries for announcements + WeChat + scheduler
- [ ] 2.3 Unit/functional: add or update tests to assert log hooks or use caplog where feasible

## 3. Rollback
- [ ] 3.1 Remove new logging config and instrumentation, fall back to console-only logging
