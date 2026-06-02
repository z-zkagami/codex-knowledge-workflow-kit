---
type: docs
created: 2026-06-02
status: active
tags:
  - demo
  - persistent-memory
---
# Demo Scenario: Cross-Session Agent Memory

This demo shows how Codex Knowledge Workflow Kit helps an AI agent resume work across sessions using an Obsidian-style vault.

## Scenario

A user captures a public note about local-first AI agent workflows. The agent routes it into research, updates active state, promotes one reusable concept, and starts the next session with enough context to continue.

## 1. Capture

The input lands in:

```text
examples/demo-vault/00_收件箱/2026-06-02-agent-workflow-capture.md
```

The note has YAML frontmatter with `type`, `created`, `status`, `source_type`, and `recommended_destination`.

## 2. Classify The Prompt

Run:

```bash
node scripts/classify-message.mjs "整理这个 agent workflow capture，判断是否进入长期研究"
```

Expected workflow hints:

```text
triage-inbox
research
```

The agent now has a concrete route instead of treating the item as a generic note.

## 3. Inject Relevant Memory

Run:

```bash
node scripts/memory-inject.mjs "agent workflow capture 长期研究"
```

The script reads the demo vault and returns:

* always-on `North Star`
* active `_state/CURRENT.md`
* relevant research, wiki, and memory notes

This gives the agent enough working context to continue without re-reading the full vault.

## 4. Route Into Research

The capture points to:

```text
examples/demo-vault/30_研究/ai-agent-workflows/
```

The research workspace keeps:

* `00_索引.md` for topic scope
* `_state/CURRENT.md` for active focus
* `_state/DECISIONS.md` for durable decisions
* `_state/HANDOFF.md` for next-session continuity

## 5. Promote Durable Knowledge

The stable concept lands in:

```text
examples/demo-vault/40_知识库/AI Agent Workflow.md
```

This separates reusable knowledge from transient research notes.

## 6. Preserve Durable Memory

The system memory layer keeps project-level continuity:

```text
examples/demo-vault/99_系统/记忆/North Star.md
examples/demo-vault/99_系统/记忆/Memories.md
examples/demo-vault/99_系统/记忆/Key Decisions.md
examples/demo-vault/99_系统/记忆/Patterns.md
examples/demo-vault/99_系统/记忆/Gotchas.md
examples/demo-vault/99_系统/记忆/Skills.md
```

These files stay small and stable so future sessions can load them cheaply.

## 7. Validate Before Commit

Run:

```bash
npm run check:layout
node scripts/validate-write.mjs examples/demo-vault/00_收件箱/2026-06-02-agent-workflow-capture.md
```

The validation checks structure, frontmatter, sensitive paths, obvious token shapes, and inbox status fields.

## What This Proves

The kit provides a runnable local memory loop:

```text
capture -> classify -> inject memory -> route -> update state -> promote knowledge -> validate
```

The value for users is practical continuity. Agents can start with project rules, retrieve relevant memory, follow known workflows, and leave a clean handoff for the next session.
