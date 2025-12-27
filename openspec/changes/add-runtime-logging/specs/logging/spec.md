## ADDED Requirements
### Requirement: Runtime log emission
System SHALL emit application logs to both stdout and a file under /opt/quoted-com-insight/logs (default app.log) with rotation limits.

#### Scenario: Container startup logging available on host
- **WHEN** the container starts with /opt/quoted-com-insight/logs mounted from the host
- **THEN** the application creates the log directory if missing and writes a startup log entry to app.log that is readable from the host

#### Scenario: Log level control
- **WHEN** LOG_LEVEL is set (fallback INFO)
- **THEN** log verbosity follows that level for both console and file sinks

### Requirement: Operational logging coverage
System SHALL record contextual logs for key operations covering announcements, WeChat commands, and schedulers.

#### Scenario: Announcements fetch and summarize
- **WHEN** fetching or summarizing announcements for a stock code
- **THEN** the system logs the code, time window, counts of announcements, and any per-code errors or summarize failures

#### Scenario: WeChat command handling
- **WHEN** processing a WeChat command (add/del/subscribe/query/refresh)
- **THEN** the system logs sanitized user identifier, command type, parameters, and errors without leaking sensitive message content

#### Scenario: Scheduler lifecycle
- **WHEN** the daily refresh scheduler starts, runs, or fails
- **THEN** the system logs the scheduled time, next-run delay, execution start/finish, and exceptions with stack traces
