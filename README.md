# Codex Knowledge Workflow Kit

Codex Knowledge Workflow Kit is Kagami's local-first workflow system for maintaining an Obsidian-style knowledge base with Codex and Agent Skills.

It packages a public, reusable version of the workflow used to move raw inputs into projects, research notes, reusable knowledge cards, and publishable content.

## What It Provides

* A CN-style vault structure for inbox, daily notes, projects, research, wiki, resources, content, and plans
* `AGENTS.md` rules for Codex-native knowledge maintenance
* Reusable Agent Skills for signal intake, inbox triage, research, writing, source extraction, and archiving
* Scripts for structure checks, RSS capture, Flomo import, QMD embedding, and shared Python environments
* Templates for daily notes, projects, wiki cards, inbox items, state handoff, signal briefs, and article drafts
* A small demo vault that is safe to inspect and run checks against

## Core Workflow

```text
external signals
  -> daily-signals
  -> triage-inbox
  -> projects / research / wiki / content / archive
  -> llm-wiki and QMD search for long-running topics
```

## Repository Layout

```text
AGENTS.md                 Codex operating rules
skills/                   Reusable Agent Skills
scripts/                  Local workflow automation
templates/                Vault and writing templates
examples/demo-vault/      Public demo vault
docs/                     Workflow and publishing notes
NOTICE.md                 Original project attribution
LICENSE                   MIT license with original and customized notices
```

## Quick Start

Run the structure check against the bundled demo vault:

```bash
bash scripts/check_cn_layout.sh
```

Use a real vault:

```bash
export CKW_VAULT_ROOT="$HOME/path/to/my-vault"
bash scripts/check_cn_layout.sh
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

This project started from an existing vault framework and evolved into Kagami's Codex-native knowledge workflow distribution. See `NOTICE.md`.
