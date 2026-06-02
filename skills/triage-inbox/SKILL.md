---
name: triage-inbox
description: Route pending inbox captures into action, project, research, wiki, content, or archive destinations inside the vault.
---

# Inbox Triage

Use this skill when the user asks to process raw captures, clean the inbox, route material, or decide what a note should become.

## Routing Destinations

- `action`: a concrete next step or checklist item.
- `project`: work that belongs in `20_Projects/`.
- `research`: material that needs a durable topic workspace in `30_Research/`.
- `wiki`: reusable knowledge that belongs in `40_Knowledge/`.
- `content`: publishable material that belongs in `60_Content/`.
- `archive`: completed, stale, or low-value material.

## Workflow

1. Read the inbox note and frontmatter.
2. Identify source type, topic, urgency, privacy level, and actionability.
3. Choose a destination and explain the routing in one short note.
4. Update frontmatter fields: `status`, `recommended_destination`, `next_step`, and `related` when useful.
5. Move or link the note only after the destination is clear.

## Output

Provide:

- Routing decision
- Reason
- Destination path
- Next action
- Validation result when a file changed

## Guardrails

- Keep raw evidence intact.
- Do not promote private or sensitive material into public demo areas.
- Prefer linking before copying when the source should remain auditable.
