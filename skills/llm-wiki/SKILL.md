---
name: llm-wiki
description: Build and maintain durable topic workspaces for long-running AI-agent memory and reusable knowledge.
---

# LLM Wiki

Use this skill when a topic should persist across sessions and accumulate research, decisions, patterns, and reusable summaries.

## Topic Workspace Shape

Create or maintain:

```text
30_Research/<topic>/
  00_Index.md
  _state/CURRENT.md
  _state/DECISIONS.md
  _state/HANDOFF.md
  sources/
  notes/
  assets/
```

Promote stable knowledge to `40_Knowledge/` when it becomes reusable outside the original project.

## Workflow

1. Define the topic boundary in `00_Index.md`.
2. Capture active state in `_state/CURRENT.md`.
3. Record durable decisions in `_state/DECISIONS.md`.
4. Keep source material under `sources/` and working notes under `notes/`.
5. Update `_state/HANDOFF.md` before ending a session.

## Guardrails

- Separate evidence from interpretation.
- Keep state files short and useful for the next agent session.
- Use QMD search or semantic recall before creating duplicate topic spaces.
