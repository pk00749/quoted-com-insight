## 1. Implementation
- [x] 1.1 Add repo checkout in deploy job (if needed) to access docker-compose.yml
- [x] 1.2 Add step to copy repo docker-compose.yml to remote /opt/quoted-com-insight/docker-compose.yml before docker compose pull/up
- [x] 1.3 Keep existing deploy flow intact (login, pull, up, prune)

## 2. Validation
- [ ] 2.1 Run `openspec validate update-dev-deploy-compose-sync --strict`
- [ ] 2.2 Dry-run or review workflow syntax for correctness

## 3. Rollback
- [ ] 3.1 Revert workflow step and rely on remote copy if sync causes issues
