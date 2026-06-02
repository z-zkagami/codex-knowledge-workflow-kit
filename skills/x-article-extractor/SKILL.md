---
name: x-article-extractor
description: Extract X/Twitter articles, threads, or single posts into local Markdown, classify them by topic, and save them into the vault.
---

# X Article Extractor

Use this skill when the user provides an X/Twitter link and asks to extract, save, or convert it into Markdown.

## Supported Inputs

- X Articles: `https://x.com/i/articles/<article_id>`
- X posts: `https://x.com/<user>/status/<tweet_id>`
- Threads when the extractor source returns thread content

## Workflow

1. Fetch the content with an available extractor or API method approved by the user.
2. Extract title, author, URL, publication date, and content type.
3. Choose a category: `skill`, `openclaw`, `opencode`, `codex`, `claude`, `ai-tools`, or `unclassified`.
4. Run `scripts/extract_x_content.py` to format and save the Markdown file.
5. Report saved path, category, content type, and any access limitations.

## Script Usage

```bash
python3 ${SKILL_DIR}/scripts/extract_x_content.py "<markdown_content>" '{"title":"Example","author":"user","url":"https://x.com/user/status/123","date":"2026-06-02","type":"tweet"}' --category=codex
```

## Category Rules

- `skill`: skill creation, workflow packs, skill governance.
- `openclaw`: OpenClaw, hooks, agent orchestration, MCP setup.
- `opencode`: editors, IDE workflows, Cursor, Windsurf, OpenCode.
- `codex`: Codex-specific coding workflows and automation.
- `claude`: Claude Code, Claude API, prompting, tool workflows.
- `ai-tools`: general AI tools and automation.
- `unclassified`: mixed or unclear material.

## Guardrails

- Private, protected, or deleted posts may be inaccessible.
- Keep images as links unless the user asks to download assets.
- Never store browser cookies, tokens, or private account data in the vault.
- Preserve original URLs for attribution.
