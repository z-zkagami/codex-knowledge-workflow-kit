# AI Memory Context Pack Template

Use this when opening a new agent window, working across tools, temporarily disabling native memory, or preventing context drift.

## Context

Current goal:

Current directory:

Existing rules:

Input material:

Existing decisions:

Output requirements:

Risk boundaries:

Verification method:

## Instructions

- Identify key constraints and forbidden actions first.
- Use QMD first when vault search is needed.
- For open-ended judgments, include counter-evidence, alternative paths, and facts still needing verification.
- Finish with changed files, verification results, and remaining risks.

## Usage Notes

- Fill only information that changes output quality.
- Put sensitive facts in the current prompt, not durable memory.
- Put active project state in `_state/`; promote stable methods to `40_Knowledge/`.
