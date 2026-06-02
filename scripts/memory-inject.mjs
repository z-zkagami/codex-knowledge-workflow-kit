#!/usr/bin/env node

import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const vaultRoot = process.env.CKW_VAULT_ROOT
  ? path.resolve(process.env.CKW_VAULT_ROOT)
  : path.join(repoRoot, "examples", "demo-vault");

const query = await readInput();
const queryTokens = tokens(query);
const markdownFiles = await collectMarkdown(vaultRoot, 300);

const scored = [];
for (const filePath of markdownFiles) {
  const text = await readFile(filePath, "utf8");
  const relative = path.relative(vaultRoot, filePath);
  const score = scoreFile(relative, text, queryTokens);
  if (score > 0) scored.push({ filePath, relative, text, score });
}

scored.sort((a, b) => b.score - a.score || a.relative.localeCompare(b.relative));

const northStarPath = path.join(vaultRoot, "99_系统", "记忆", "North Star.md");
const northStar = await readSnippet(northStarPath, 900);
const currentFiles = await collectMatching(vaultRoot, (filePath) => filePath.endsWith(path.join("_state", "CURRENT.md")), 6);

const lines = ["# Memory Injection", "", `Vault root: ${vaultRoot}`];

if (query.trim()) lines.push(`Query: ${query.trim().slice(0, 300)}`);
lines.push("");

if (northStar) {
  lines.push("## Always-On Memory", "", "### 99_系统/记忆/North Star.md", northStar, "");
}

if (currentFiles.length) {
  lines.push("## Active Working State");
  for (const filePath of currentFiles) {
    lines.push("", `### ${path.relative(vaultRoot, filePath)}`);
    lines.push(await readSnippet(filePath, 700));
  }
  lines.push("");
}

const relevant = scored
  .filter((item) => item.relative !== "99_系统/记忆/North Star.md")
  .slice(0, 5);

if (relevant.length) {
  lines.push("## Relevant Vault Notes");
  for (const item of relevant) {
    lines.push("", `### ${item.relative}`);
    lines.push(snippet(item.text, queryTokens, 900));
  }
  lines.push("");
} else {
  lines.push("## Relevant Vault Notes", "", "No direct vault match. Use AGENTS.md and workflow hints first.", "");
}

lines.push("## Use This Context For", "");
lines.push("- recovering project direction");
lines.push("- choosing the next workflow");
lines.push("- avoiding duplicate research");
lines.push("- updating _state or 99_系统/记忆 after durable changes");

process.stdout.write(`${lines.join("\n")}\n`);

async function readInput() {
  const argText = process.argv.slice(2).join(" ");
  if (process.stdin.isTTY) return argText;
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const stdinText = Buffer.concat(chunks).toString("utf8");
  const raw = `${argText}\n${stdinText}`.trim();
  try {
    const parsed = JSON.parse(raw);
    return JSON.stringify(parsed);
  } catch {
    return raw;
  }
}

function tokens(text) {
  const normalized = text.toLowerCase();
  const ascii = normalized.match(/[a-z0-9][a-z0-9_-]{1,}/g) ?? [];
  const cjkChars = [...normalized].filter((char) => /[\u4e00-\u9fff]/u.test(char));
  const cjk = [];
  for (let index = 0; index < cjkChars.length - 1; index += 1) {
    cjk.push(`${cjkChars[index]}${cjkChars[index + 1]}`);
  }
  return [...new Set([...ascii, ...cjk])].slice(0, 80);
}

function scoreFile(relative, text, queryTokens) {
  const haystack = `${relative}\n${text}`.toLowerCase();
  const pathBoost = relative.includes("99_系统/记忆/") || relative.includes("_state/") ? 2 : 0;
  if (!queryTokens.length) return pathBoost;
  let score = pathBoost;
  for (const token of queryTokens) {
    if (haystack.includes(token)) score += relative.toLowerCase().includes(token) ? 3 : 1;
  }
  return score;
}

function snippet(text, queryTokens, maxChars) {
  const trimmed = text.trim();
  if (!queryTokens.length) return trimmed.slice(0, maxChars);
  const lower = trimmed.toLowerCase();
  const firstHit = queryTokens
    .map((token) => lower.indexOf(token))
    .filter((index) => index >= 0)
    .sort((a, b) => a - b)[0];
  if (firstHit === undefined) return trimmed.slice(0, maxChars);
  const start = Math.max(0, firstHit - 240);
  return trimmed.slice(start, start + maxChars);
}

async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readSnippet(filePath, maxChars) {
  if (!(await exists(filePath))) return "";
  const text = await readFile(filePath, "utf8");
  return text.trim().slice(0, maxChars);
}

async function collectMarkdown(root, limit) {
  return collectMatching(root, (filePath) => filePath.endsWith(".md"), limit);
}

async function collectMatching(root, predicate, limit) {
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
