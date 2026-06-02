# Codex Adapter

This adapter installs `AGENTS.md` and `.codex/hooks.json` into a vault.

Run:

```bash
export CKW_KIT_ROOT="/path/to/codex-knowledge-workflow-kit"
export CKW_VAULT_ROOT="/path/to/your-vault"
node "$CKW_KIT_ROOT/scripts/init-kit.mjs" --vault "$CKW_VAULT_ROOT" --tool codex
```
