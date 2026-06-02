# Codex Persistent Memory Adapter

Use this vault as the shared persistent memory layer for Codex sessions.

## Startup

Run:

```bash
node "$CKW_KIT_ROOT/scripts/session-start.mjs"
```

## Prompt Routing

For user prompts that reference vault work, run:

```bash
node "$CKW_KIT_ROOT/scripts/classify-message.mjs" "<prompt>"
node "$CKW_KIT_ROOT/scripts/memory-inject.mjs" "<prompt>"
```

## Write Safety

After Markdown writes, run:

```bash
node "$CKW_KIT_ROOT/scripts/validate-write.mjs" "<changed-file.md>"
```

## Durable Memory

* Stable rules live in `AGENTS.md`.
* Durable memory lives in `99_System/Memory/`.
* Project continuity lives in `_state/CURRENT.md`, `_state/DECISIONS.md`, and `_state/HANDOFF.md`.
* Searchable recall uses QMD when available.
