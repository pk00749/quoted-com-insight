## ADDED Requirements
### Requirement: Configurable log level and path
System SHALL expose `log_level` (default INFO) and `log_path` (default /opt/quoted-com-insight/logs/app.log) via YAML and environment variables.

#### Scenario: Missing keys
- **WHEN** YAML omits `log_level` or `log_path` and no environment override is present
- **THEN** the system defaults to INFO level and /opt/quoted-com-insight/logs/app.log

#### Scenario: Environment override
- **WHEN** LOG_LEVEL or LOG_PATH is provided in the environment
- **THEN** the system uses those values for logging configuration
