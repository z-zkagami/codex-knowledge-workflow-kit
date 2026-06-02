# Gemini CLI Persistent Memory Adapter

Use this vault as the shared persistent memory layer for Gemini CLI sessions.

## Context Commands

```bash
node "$CKW_KIT_ROOT/scripts/session-start.mjs"
node "$CKW_KIT_ROOT/scripts/classify-message.mjs" "<prompt>"
node "$CKW_KIT_ROOT/scripts/memory-inject.mjs" "<prompt>"
```

## Working Rules

* Treat `99_System/Memory/` as durable cross-session memory.
* Treat `_state/` files as active project continuity.
* Treat `40_Knowledge/` as reusable concepts and judgments.
* Run `node "$CKW_KIT_ROOT/scripts/validate-write.mjs" "<changed-file.md>"` after Markdown writes.
