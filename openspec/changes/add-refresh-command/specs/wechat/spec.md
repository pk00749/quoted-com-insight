## ADDED Requirements
### Requirement: Refresh Command Implementation
System SHALL support immediate summary regeneration using pattern ^refresh\d{6}$ reusing existing summarize flow.

#### Scenario: Immediate refresh success
- **WHEN** user sends refresh+code and generation succeeds
- **THEN** system regenerates and saves summary, updates timestamp, and reply text SHALL be `<code> 已刷新，YYYY-MM-DD HH:MM` (Beijing time)

#### Scenario: Refresh failure
- **WHEN** generation fails
- **THEN** system returns friendly error message

#### Scenario: Rate limit
- **WHEN** user refreshes same code within limit window
- **THEN** system returns rate limit notice

