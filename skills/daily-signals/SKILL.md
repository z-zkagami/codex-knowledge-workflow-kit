---
name: daily-signals
description: Capture public AI/newsletter signals into the vault, produce a daily signal brief, and route durable findings into inbox, research, wiki, content, or archive.
---

# Daily Signals

Use this skill when the user asks to review public AI signals, newsletters, RSS items, daily digests, or items worth reading today.

## Workflow

1. Collect public sources or run the bundled RSS fetcher when appropriate.
2. Write raw captures under `50_Resources/Newsletters/` or `50_Resources/Signal_Briefs/`.
3. Deduplicate obvious repeats and group items by theme.
4. Mark each item as `research`, `wiki`, `content`, `archive`, or `ignore`.
5. Promote durable items into `00_Inbox/`, a research workspace, or a wiki note.

## Output

Return a compact brief:

- Best item today
- Useful scan items
- Content or research opportunities
- Files created or updated
- Follow-up routing

## Guardrails

- Use public source material only.
- Keep raw sources separate from durable judgments.
- Avoid storing account tokens, cookies, private URLs, or unpublished work material.
- Run `scripts/validate-write.mjs` when new Markdown files are created.
