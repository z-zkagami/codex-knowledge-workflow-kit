# Claude Code Adapter

This adapter installs `CLAUDE.md` and `.claude/rules/persistent-memory.md`.

Run:

```bash
export CKW_KIT_ROOT="/path/to/codex-knowledge-workflow-kit"
export CKW_VAULT_ROOT="/path/to/your-vault"
node "$CKW_KIT_ROOT/scripts/init-kit.mjs" --vault "$CKW_VAULT_ROOT" --tool claude-code
```
