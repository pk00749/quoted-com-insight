#### Scenario: Query stock code
- **WHEN** user sends 6-digit code
- **THEN** query handler processes and returns summary

## ADDED Requirements
### Requirement: Offline Command Testability
System SHALL allow command handlers to be unit tested without external network.

#### Scenario: Mock summarize
- **WHEN** test injects fake summarize_announcements
- **THEN** handler returns deterministic result
## MODIFIED Requirements
### Requirement: WeChat Text Command Handling
System SHALL delegate each supported command to isolated handler modules.

#### Scenario: Add command module
- **WHEN** user sends addXXXXXX
- **THEN** dispatcher invokes add handler returning result


