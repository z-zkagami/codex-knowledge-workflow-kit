# Codex Knowledge Workflow Kit

Codex Knowledge Workflow Kit is Kagami's local-first persistent memory layer for AI agents.

It turns an Obsidian-style Markdown vault into a versioned, searchable, editable working memory for Codex, Claude Code, Gemini CLI, and other agent tools. Agents can resume across sessions with the same goals, rules, active projects, research state, and output workflows.

## Architecture

### Memory Layer

The vault stores durable working memory:

* `AGENTS.md` defines project rules and collaboration behavior
* `99_系统/记忆/` stores north star, memories, decisions, patterns, gotchas, and skill notes
* `_state/CURRENT.md`, `_state/DECISIONS.md`, and `_state/HANDOFF.md` preserve topic and project continuity
* `vault-manifest.json` describes the vault shape, required files, QMD index, and validation rules

### Workflow Layer

Agent Skills turn raw input into concrete movement:

* `daily-signals` captures public AI signals
* `triage-inbox` routes captures into action, project, research, knowledge, content, or archive
* `llm-wiki`, `research`, and `parse-knowledge` maintain long-running topics
* `wechat-*` skills move material through angle, outline, style, draft, and title gates
* `archive` keeps active spaces clean

### Retrieval Layer

QMD and local embeddings make vault memory searchable:

* semantic recall over Markdown notes
* duplicate and related-topic discovery
* reusable context packs for future agent sessions
* Qwen3 embedding defaults for Chinese-heavy vaults

## What It Provides

* A CN-style demo vault for inbox, daily notes, projects, research, wiki, resources, content, plans, and system memory
* Codex hook examples for session start, prompt classification, memory injection, write validation, and stop checks
* Scripts for structure checks, session context injection, prompt-based memory injection, message classification, Markdown validation, RSS capture, Flomo import, QMD embedding, and shared Python environments
* Tool adapters for Codex, Claude Code, Gemini CLI, and Cursor
* Reusable templates for daily notes, projects, wiki cards, inbox items, state handoff, signal briefs, and article drafts

## Core Loop

```text
external signals
  -> daily-signals
  -> triage-inbox
  -> project / research / wiki / content / archive
  -> _state + 99_系统/记忆 + QMD
  -> next agent session resumes from persistent memory
```

## Repository Layout

```text
AGENTS.md                 Agent operating rules
.codex/                   Hook examples for Codex
vault-manifest.json       Vault metadata and validation contract
adapters/                 Tool-specific adapter files
skills/                   Reusable Agent Skills
scripts/                  Local workflow automation
templates/                Vault and writing templates
examples/demo-vault/      Public demo vault
docs/                     Workflow and persistent memory notes
docs/demo-scenario.md     End-to-end cross-session memory demo
docs/extending.md         Extension model and adapter guide
NOTICE.md                 Original project attribution
LICENSE                   MIT license with original and customized notices
```

## Quick Start

Initialize a real vault with the Codex adapter:

```bash
node scripts/init-kit.mjs --vault "$HOME/path/to/my-vault" --tool codex
```

Install every bundled adapter:

```bash
node scripts/init-kit.mjs --vault "$HOME/path/to/my-vault" --tool all
```

Run the structure check against the bundled demo vault:

```bash
bash scripts/check_cn_layout.sh
```

Use a real vault:

```bash
export CKW_VAULT_ROOT="$HOME/path/to/my-vault"
bash scripts/check_cn_layout.sh
```

Preview session-start memory context:

```bash
node scripts/session-start.mjs
```

Classify a prompt into workflow hints:

```bash
node scripts/classify-message.mjs "整理今天的 AI 信号，看看哪些值得进入研究"
```

Inject relevant vault memory for a prompt:

```bash
node scripts/memory-inject.mjs "agent workflow capture 长期研究"
```

Validate Markdown writes:

```bash
node scripts/validate-write.mjs examples/demo-vault/00_收件箱/2026-06-02-agent-workflow-capture.md
```

Walk through the full memory loop:

```bash
open docs/demo-scenario.md
```

Review extension points:

```bash
open docs/extending.md
```

Create shared Python environment roots:

```bash
bash scripts/workspace_env.sh doctor
eval "$(bash scripts/workspace_env.sh exports)"
```

Fetch AI HOT RSS into the configured vault:

```bash
python3 scripts/fetch_aihot.py --date 2026-06-02
```

Sync Flomo into the inbox:

```bash
export FLOMO_SECRET="your-flomo-signing-secret"
python3 scripts/flomo_sync_to_inbox.py --config-path "$HOME/path/to/flomo/config.json"
```

Refresh QMD embeddings:

```bash
export CKW_QMD_CONFIG="$HOME/.config/qmd/my-vault.yml"
export CKW_QMD_DB="$HOME/.cache/qmd/my-vault.sqlite"
node scripts/qmd/embed_cn_qwen3.mjs
```

## Included Skills

Knowledge operations:

* `daily-signals`
* `triage-inbox`
* `llm-wiki`
* `research`
* `parse-knowledge`
* `archive`

Content workflow:

* `wechat-material-intake`
* `wechat-topic-outline-planner`
* `wechat-style-profiler`
* `wechat-draft-writer`
* `wechat-title-generator`

Source intake:

* `x-article-extractor`
* `youtube-transcript`
* `paper-summary`

## Public Version Scope

This repository contains reusable workflow assets and a demo vault. Personal notes, unpublished drafts, private sync states, account tokens, and work-sensitive source material stay outside the public release.

## Attribution

This project started from an existing vault framework and evolved into Kagami's persistent memory layer for AI agents. See `NOTICE.md`.
