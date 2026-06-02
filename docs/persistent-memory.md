# Persistent Memory

Codex Knowledge Workflow Kit uses Obsidian Markdown as a shared working memory layer for AI agents.

## Memory Layers

### 1. Repository Rules

`AGENTS.md` stores stable behavior:

* directory contracts
* workflow entrypoints
* privacy rules
* validation commands
* collaboration expectations

These rules are committed to Git and shared by every agent using the repository.

### 2. Vault Memory

`99_系统/记忆/` stores durable working memory:

* `North Star.md`: project direction and durable goals
* `Memories.md`: stable context worth carrying across sessions
* `Key Decisions.md`: decisions that shape future work
* `Patterns.md`: repeatable ways of working
* `Gotchas.md`: failure modes and safeguards
* `Skills.md`: skill map and routing notes

Topic-specific continuity stays near the work in `_state/CURRENT.md`, `_state/DECISIONS.md`, and `_state/HANDOFF.md`.

### 3. Agent Native Memories

Codex or other tools may maintain their own native memories. Treat those as personal recall and session summaries. The vault remains the shared source of project truth.

### 4. Retrieval

QMD indexes the Markdown vault for semantic recall. Use QMD to find related notes, avoid duplicates, and inject compact context into future sessions.

## Hook Flow

The hook examples support a minimal lifecycle:

* `SessionStart`: read the north star, active state files, and recent briefs
* `UserPromptSubmit`: classify the user prompt into likely workflows
* `PostToolUse`: validate Markdown files after writes
* `Stop`: run a final lightweight checklist

The example hooks call scripts in `scripts/` and use `CKW_VAULT_ROOT` to target a real vault.

## Memory Hygiene

Keep stable project context in the vault. Keep credentials, raw sync states, unpublished private drafts, and sensitive work material outside the public repository.

Use `scripts/validate-write.mjs` before committing Markdown changes that affect the vault.
