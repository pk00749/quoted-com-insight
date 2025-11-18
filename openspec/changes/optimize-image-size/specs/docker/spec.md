## ADDED Requirements
### Requirement: Multi-stage Docker Build
System SHALL build production image via multi-stage to minimize final size.

#### Scenario: Build success
- **WHEN** executing docker build
- **THEN** final image excludes build-only dependencies

### Requirement: Chromium Only Browser Install
System SHALL install only Chromium for Playwright to reduce size.

#### Scenario: Browser availability
- **WHEN** running Playwright tasks
- **THEN** Chromium launches successfully

