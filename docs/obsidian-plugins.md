---
type: docs
created: 2026-06-02
status: active
tags:
  - obsidian
  - plugins
---
# Obsidian Plugin Stack

This list is based on the local vault plugin inventory used while building the kit. It is safe to publish because it records plugin names and public metadata only.

## Active Local Plugin Inventory

| Plugin | ID | Version | Role |
| --- | --- | --- | --- |
| HTML Reader | `obsidian-html-plugin` | `1.0.13` | Opens `.html` and `.htm` files inside Obsidian. |
| Excalidraw | `obsidian-excalidraw-plugin` | `2.22.0` | Adds visual sketching, diagrams, and canvas-like thinking. |
| Claudian | `claudian` | `1.3.71` | Embeds Claude Code as an AI collaborator inside the vault. |
| Terminal | `terminal` | `3.23.0` | Provides terminal access from Obsidian. |
| Git | `obsidian-git` | `2.38.0` | Adds Git backup, versioning, and sync workflows. |

## Recommended Minimal Stack

For users who want the kit to work with minimal setup:

1. **Git**
   Use it to keep vault changes versioned and recoverable.

2. **Terminal**
   Use it to run kit scripts without leaving Obsidian.

3. **Claudian or another agent bridge**
   Use it when you want an AI coding agent to operate directly inside the vault.

## Recommended Power-User Stack

For users who want richer workflows:

1. **Git** for versioned memory and rollback.
2. **Terminal** for local automation.
3. **Claudian** for in-vault Claude Code collaboration.
4. **Excalidraw** for diagrams and visual research.
5. **HTML Reader** for local HTML source review.

## Notes

Plugins are optional. The kit works from the command line with Node.js and Python, and Obsidian remains the editable memory interface.

Do not commit `.obsidian/plugins/*/data.json` or other plugin state files to a public repository. Plugin state can contain local paths, workspace layout, or personal preferences.
