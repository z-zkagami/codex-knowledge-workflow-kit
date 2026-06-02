# Persistent Memory Notes

Use Codex Knowledge Workflow Kit scripts to recover context and route work.

```bash
node "$CKW_KIT_ROOT/scripts/session-start.mjs"
node "$CKW_KIT_ROOT/scripts/memory-inject.mjs" "<prompt>"
```

Keep shared memory in the vault so Codex, Claude Code, Gemini CLI, and other tools can reuse it.
