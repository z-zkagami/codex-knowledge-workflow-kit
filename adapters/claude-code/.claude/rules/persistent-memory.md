# Persistent Memory Rule

When the user asks about vault work, long-running research, content workflow, or project continuity:

1. Run `node "$CKW_KIT_ROOT/scripts/classify-message.mjs" "<prompt>"`.
2. Run `node "$CKW_KIT_ROOT/scripts/memory-inject.mjs" "<prompt>"`.
3. Use `AGENTS.md`, `99_System/Memory/`, and `_state/` as shared project truth.
4. Run `node "$CKW_KIT_ROOT/scripts/validate-write.mjs" "<changed-file.md>"` after Markdown writes.

Store durable cross-tool facts in the vault. Store personal Claude-specific preferences in Claude native memory.
