---
type: docs
created: 2026-06-02
status: active
tags:
  - extensibility
  - adapters
  - workflow-packs
---
# Extending Codex Knowledge Workflow Kit

Codex Knowledge Workflow Kit is designed for two user types:

* lazy users who want one command and a working vault
* builders who want to swap tools, workflows, retrieval, and validation rules

The core contract is:

```text
core memory kit
  + tool adapter
  + workflow pack
  + retrieval provider
  + validation rules
  + personal vault config
```

## One-Command Setup

Run:

```bash
node scripts/init-kit.mjs --vault "$HOME/Vault" --tool codex
```

Install every bundled adapter:

```bash
node scripts/init-kit.mjs --vault "$HOME/Vault" --tool all
```

Preview first:

```bash
node scripts/init-kit.mjs --vault "$HOME/Vault" --tool all --dry-run
```

The initializer creates the core vault structure, memory files, `vault-manifest.json`, and selected adapter files.

## Vault Contract

`vault-manifest.json` is the shared contract. It declares:

* directory roots
* memory files
* state file names
* infrastructure files
* required frontmatter
* default QMD index metadata

When a user customizes the vault layout, update the manifest first, then adapt scripts and validators.

## Tool Adapters

Adapters live under `adapters/<tool>/`.

Each adapter has:

```text
adapter.json
README.md
tool-specific files
```

Example `adapter.json`:

```json
{
  "name": "codex",
  "displayName": "Codex",
  "files": [
    {
      "source": "AGENTS.md",
      "target": "AGENTS.md"
    }
  ]
}
```

Bundled adapters:

* `codex`: installs `AGENTS.md` and `.codex/hooks.json`
* `claude-code`: installs `CLAUDE.md` and `.claude/rules/persistent-memory.md`
* `gemini-cli`: installs `GEMINI.md` and `.gemini/persistent-memory.md`
* `cursor`: installs `.cursor/rules/persistent-memory.mdc`

Adapter files should call scripts through `CKW_KIT_ROOT` and target vaults through `CKW_VAULT_ROOT`.

## Workflow Packs

Workflow packs currently live in `skills/`.

A mature pack should include:

```text
skills/<pack>/
  SKILL.md
  scripts/
  references/
  templates/
```

Use a workflow pack when a repeated process needs routing, examples, scripts, or domain-specific rules.

Good packs:

* name their trigger conditions clearly
* state where files should land
* preserve raw source material
* separate AI synthesis from human judgment
* define validation or handoff steps

## Retrieval Providers

QMD is the default retrieval provider. The current minimal path is:

```bash
node scripts/memory-inject.mjs "<prompt>"
```

Future providers can implement the same practical contract:

```text
input: prompt + vault root + manifest
output: compact Markdown context block
```

Candidate providers:

* `qmd`
* `rg`
* `sqlite`
* `chroma`
* `lancedb`
* `obsidian-local-rest-api`

Keep provider output compact enough for agent startup context.

## Validators

Validators protect the public and private boundary.

Current validator:

```bash
node scripts/validate-write.mjs "<changed-file.md>"
```

Validation should cover:

* required frontmatter
* private local paths
* obvious token shapes
* inbox status fields
* generated cache directories
* binary and database files before public release

## Extension Checklist

When adding an extension:

1. Add a small example.
2. Add a README or docs section.
3. Add it to `vault-manifest.json` when it becomes infrastructure.
4. Add a `node --check` or shell check if it ships executable code.
5. Run `npm run check:layout`, `npm run check:python`, and `npm run check:node`.
6. Run a sensitive-string scan before committing.

## OSS Maintenance Use

For open-source maintainers, the kit can support:

* PR review memory
* issue triage routing
* release checklist continuity
* contributor onboarding context
* security and structure checks
* session handoff between different AI tools

This is the main application story for Codex for Open Source: reduce repeated context loading and make maintenance workflows easier to inspect, validate, and share.
