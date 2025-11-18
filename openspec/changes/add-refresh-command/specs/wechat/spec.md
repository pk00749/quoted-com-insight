## ADDED Requirements
### Requirement: Refresh Command Implementation
System SHALL support immediate summary regeneration using pattern ^refresh\d{6}$ reusing existing summarize flow.

#### Scenario: Immediate refresh success
- **WHEN** user sends refresh+code and generation succeeds
- **THEN** cached JSON and timestamp updated and result returned

#### Scenario: Refresh failure
- **WHEN** generation fails
- **THEN** system returns friendly error message

#### Scenario: Rate limit
- **WHEN** user refreshes same code within limit window
- **THEN** system returns rate limit notice

