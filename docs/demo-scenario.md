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
examples/demo-vault/00_Inbox/2026-06-02-agent-workflow-capture.md
```

The note has YAML frontmatter with `type`, `created`, `status`, `source_type`, and `recommended_destination`.

## 2. Classify The Prompt

Run:

```bash
node scripts/classify-message.mjs "Review this agent workflow capture and decide whether it belongs in long-running research"
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
node scripts/memory-inject.mjs "agent workflow capture long-running research"
```

The script reads the demo vault and returns:

* always-on `North Star`
* active `_state/CURRENT.md`
* relevant research, wiki, and memory notes

This gives the agent enough working context to continue without re-reading the full vault.

## 4. Route Into Research

The capture points to:

```text
examples/demo-vault/30_Research/ai-agent-workflows/
```

The research workspace keeps:

* `00_Index.md` for topic scope
* `_state/CURRENT.md` for active focus
* `_state/DECISIONS.md` for durable decisions
* `_state/HANDOFF.md` for next-session continuity

## 5. Promote Durable Knowledge

The stable concept lands in:

```text
examples/demo-vault/40_Knowledge/AI Agent Workflow.md
```

This separates reusable knowledge from transient research notes.

## 6. Preserve Durable Memory

The system memory layer keeps project-level continuity:

```text
examples/demo-vault/99_System/Memory/North Star.md
examples/demo-vault/99_System/Memory/Memories.md
examples/demo-vault/99_System/Memory/Key Decisions.md
examples/demo-vault/99_System/Memory/Patterns.md
examples/demo-vault/99_System/Memory/Gotchas.md
examples/demo-vault/99_System/Memory/Skills.md
```

These files stay small and stable so future sessions can load them cheaply.

## 7. Validate Before Commit

Run:

```bash
npm run check:layout
node scripts/validate-write.mjs examples/demo-vault/00_Inbox/2026-06-02-agent-workflow-capture.md
```

The validation checks structure, frontmatter, sensitive paths, obvious token shapes, and inbox status fields.

## What This Proves

The kit provides a runnable local memory loop:

```text
capture -> classify -> inject memory -> route -> update state -> promote knowledge -> validate
```

The value for users is practical continuity. Agents can start with project rules, retrieve relevant memory, follow known workflows, and leave a clean handoff for the next session.
