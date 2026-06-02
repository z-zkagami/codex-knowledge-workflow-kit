#!/usr/bin/env node

import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const vaultRoot = process.env.CKW_VAULT_ROOT
  ? path.resolve(process.env.CKW_VAULT_ROOT)
  : path.join(repoRoot, "examples", "demo-vault");

async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readSnippet(filePath, maxChars = 1200) {
  if (!(await exists(filePath))) return "";
  const text = await readFile(filePath, "utf8");
  return text.trim().slice(0, maxChars);
}

async function walk(root, predicate, limit = 8) {
  const results = [];
  async function visit(dir) {
    if (results.length >= limit || !(await exists(dir))) return;
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (results.length >= limit) return;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await visit(fullPath);
      } else if (predicate(fullPath)) {
        results.push(fullPath);
      }
    }
  }
  await visit(root);
  return results;
}

function rel(filePath) {
  return path.relative(vaultRoot, filePath);
}

const northStar = await readSnippet(path.join(vaultRoot, "99_系统", "记忆", "North Star.md"));
const currentFiles = await walk(vaultRoot, (filePath) => filePath.endsWith(path.join("_state", "CURRENT.md")), 6);
const briefFiles = await walk(path.join(vaultRoot, "50_资源", "信号简报"), (filePath) => filePath.endsWith(".md"), 5);

const lines = [
  "# Persistent Memory Context",
  "",
  `Vault root: ${vaultRoot}`,
  "",
];

if (northStar) {
  lines.push("## North Star", "", northStar, "");
}

if (currentFiles.length) {
  lines.push("## Active State Files");
  for (const filePath of currentFiles) {
    const snippet = await readSnippet(filePath, 600);
    lines.push("", `### ${rel(filePath)}`, snippet);
  }
  lines.push("");
}

if (briefFiles.length) {
  lines.push("## Recent Signal Briefs");
  for (const filePath of briefFiles.slice(-3)) {
    lines.push(`- ${rel(filePath)}`);
  }
  lines.push("");
}

lines.push("## Routing Reminder", "");
lines.push("- Use AGENTS.md for stable rules.");
lines.push("- Use 99_系统/记忆 for durable cross-session memory.");
lines.push("- Use _state files for active project continuity.");
lines.push("- Use QMD for semantic recall when exact paths are unknown.");

process.stdout.write(`${lines.join("\n")}\n`);
