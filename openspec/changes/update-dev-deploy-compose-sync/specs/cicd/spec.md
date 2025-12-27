## ADDED Requirements
### Requirement: Sync compose file before remote deploy
System SHALL copy the repository's docker-compose.yml to the remote deploy host before executing docker compose commands in the dev pipeline.

#### Scenario: Dev deploy run
- **WHEN** the cicd-dev workflow deploy job executes
- **THEN** docker-compose.yml from the repository is placed at /opt/quoted-com-insight/docker-compose.yml on the remote host before docker compose pull/up
