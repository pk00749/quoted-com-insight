# Change: Sync docker-compose.yml to remote before dev deploy

## Why
- Remote deploy job currently runs docker compose on the cloud instance without syncing the compose file from the repository, risking drift between code and runtime.

## What Changes
- In `workflows/cicd-dev.yml`, add a step to copy the repository `docker-compose.yml` to the remote instance before running `docker compose pull`/`up`.

## Impact
- Affected specs: cicd (deployment automation)
- Affected code: .github/workflows/cicd-dev.yml
