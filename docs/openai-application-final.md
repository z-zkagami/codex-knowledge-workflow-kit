---
type: docs
created: 2026-06-02
status: active
tags:
  - application
  - openai
  - codex-for-oss
---
# OpenAI Codex For OSS Application Draft

## Repository

```text
https://github.com/z-zkagami/codex-knowledge-workflow-kit
```

## Project Summary

```text
codex-knowledge-workflow-kit is a local-first persistent memory layer for AI agents. It turns an Obsidian-style Markdown vault into shared project memory for Codex, Claude Code, Gemini CLI, and Cursor, with adapters, workflow packs, retrieval scripts, validation checks, and a public demo vault. It helps maintainers preserve issue triage rules, PR review context, release handoffs, gotchas, and reusable workflows across sessions.
```

## API Credit Usage

```text
API credits will support OSS maintenance automation: issue and PR triage summaries, review of adapter/manifest/validator changes, release-readiness checks, session transcript distillation into durable memory updates, and setup guidance for users adapting the kit to their own vaults. The goal is to reduce repeated context loading and make AI-assisted maintenance workflows easier to inspect, validate, and share.
```

## Fit Notes

The project is public, local-first, and built around Codex-compatible maintenance workflows. It provides:

* one-command vault initialization
* adapters for Codex, Claude Code, Gemini CLI, and Cursor
* persistent memory files for goals, decisions, patterns, gotchas, and skills
* session-start and prompt-based memory injection scripts
* validation checks for layout, frontmatter, and public safety
* GitHub Actions for repeatable CI

The strongest application angle is open-source maintenance continuity: issue triage, PR review memory, release handoff, contributor onboarding, and project-specific gotcha preservation.
