## MODIFIED Requirements
### Requirement: Configurable Daily Subscription Refresh Time
System SHALL schedule daily summary generation by `subscription_refresh_time` (HH:MM Asia/Shanghai).

#### Scenario: Valid time
- **WHEN** value matches HH:MM and in range
- **THEN** scheduler sets next run accordingly

#### Scenario: Invalid format
- **WHEN** pattern fails or out of range
- **THEN** fallback to default 09:00 with warning

