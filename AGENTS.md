# Agent Behavior - Codex Knowledge Workflow Kit

Act as a local-first knowledge workflow operator. Keep inputs moving through capture, triage, research, reusable knowledge, and publishable output.

## Structure

* `00_收件箱`: quick captures and imported signals, processed by `triage-inbox`
* `10_日记`: daily logs and work journals
* `20_项目`: active projects using C.A.P. layout
* `30_研究`: persistent topic workspaces, including `llm-wiki`
* `40_知识库`: atomic concepts and reusable judgments
* `50_资源`: curated signals, newsletters, style references, and staging
* `60_内容中台`: public output pipelines such as articles and social posts
* `90_计划`: execution plans
* `99_系统`: templates, rules, and archives

## Core Workflows

* `daily-signals`: turn public AI signals into a daily brief
* `triage-inbox`: route new captures into action, project, research, knowledge, content, or archive
* `llm-wiki`: maintain long-running topic workspaces
* `research`: plan and execute deeper research
* `parse-knowledge`: turn unstructured notes into vault-ready Markdown
* `archive`: move completed work out of active space

## Content Workflows

* `wechat-material-intake`: convert raw tinkering notes into writing inputs
* `wechat-topic-outline-planner`: turn rough material into article angles and outlines
* `wechat-style-profiler`: build a reusable author style profile
* `wechat-draft-writer`: write a draft from confirmed structure and style DNA
* `wechat-title-generator`: generate and score article titles and summaries

## Source Intake

* `x-article-extractor`: save X articles and threads as Markdown
* `youtube-transcript`: fetch YouTube transcripts
* `paper-summary`: parse and summarize academic papers

## Rules

* Preserve original source material and keep AI synthesis separate from human judgment.
* Promote stable findings from `30_研究` into `40_知识库`.
* Keep long-running topics stateful with `CURRENT.md`, `DECISIONS.md`, and `HANDOFF.md`.
* Run `bash scripts/check_cn_layout.sh` before publishing structure changes.
* Use `CKW_VAULT_ROOT` to point scripts at a real vault.
* Keep private notes, tokens, raw sync states, and unpublished work outside the public repository.
