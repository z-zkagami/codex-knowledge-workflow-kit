# Workflow

## Intake

`daily-signals` collects public AI signals and stores a brief in `50_Resources/Signal_Briefs`.

`flomo_sync_to_inbox.py` can import personal captures into `00_Inbox` when `FLOMO_SECRET` and a local Flomo config are available.

## Triage

`triage-inbox` routes each item into one destination:

* action
* project
* research topic
* atomic knowledge card
* content material
* archive

## Research

`research` creates a plan and executes deep topic work. `llm-wiki` keeps long-running topics stateful under `30_Research/<topic>/llm-wiki`.

## Knowledge

Stable concepts move to `40_Knowledge`. QMD embeddings can index the vault for local semantic search.

## Content

The `wechat-*` skills convert raw material into angle selection, outline, style profile, draft, title, and publishing metadata.
