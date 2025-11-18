## ADDED Requirements
### Requirement: Conditional Database Initialization
System SHALL skip subscription DB schema creation if existing file detected.

#### Scenario: DB exists
- **WHEN** subscriptions.db file present
- **THEN** system logs skip and proceeds

#### Scenario: DB missing
- **WHEN** file absent
- **THEN** system creates schema tables

