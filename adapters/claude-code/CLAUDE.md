# Claude Code Persistent Memory Adapter

Use this vault as the shared persistent memory layer for Claude Code sessions.

## Memory Loading

At session start, read:

```bash
node "$CKW_KIT_ROOT/scripts/session-start.mjs"
```

For task prompts, gather relevant context:

```bash
node "$CKW_KIT_ROOT/scripts/memory-inject.mjs" "<prompt>"
```

## Project Rules

* Keep stable project instructions concise.
* Keep user-specific preferences in Claude native memory.
* Keep shared project memory in `99_系统/记忆/`.
* Keep task continuity near the work in `_state/`.
* Validate Markdown writes before committing.
