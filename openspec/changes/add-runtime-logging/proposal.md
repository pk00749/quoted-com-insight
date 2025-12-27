# Change: Add runtime logging and host visibility

## Why
- Running containers currently do not emit application logs to the host directory /opt/quoted-com-insight/logs, making troubleshooting difficult.
- Core operations (API calls, announcement fetch/summarize, WeChat commands) lack consistent structured logging, limiting observability.

## What Changes
- Add an application logging configuration that writes to both console and a file under /opt/quoted-com-insight/logs with rotation safeguards, aligned to configurable log level.
- Ensure the container creates and writes to the host-mounted log path so operators can tail logs from the host.
- Instrument key operations (API handlers, announcement fetch/summarize, WeChat command flows) with contextual info and error details.

## Impact
- Affected specs: logging (new capability)
- Affected code: FastAPI startup/config, routers (announcements/system/wechat), services (announcement/subscription), settings/env for log level and log path
