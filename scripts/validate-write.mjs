#!/usr/bin/env node

import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const vaultRoot = process.env.CKW_VAULT_ROOT
  ? path.resolve(process.env.CKW_VAULT_ROOT)
  : path.join(repoRoot, "examples", "demo-vault");

const explicitPaths = process.argv.slice(2).filter((item) => item.endsWith(".md"));
const files = explicitPaths.length ? explicitPaths.map((item) => path.resolve(item)) : await collectMarkdown(vaultRoot, 40);

const secretPatterns = [
  /sk-[A-Za-z0-9_-]{20,}/,
  /\/Users\/kagami/,
  /192\.168\.\d+\.\d+/,
  /FLOMO_SECRET\s*=\s*"[^"]+"/,
  /\b(?:private|internal|personal)[-_ ]?(?:account|user|id)\b/i,
];

let failures = 0;

for (const filePath of files) {
  const text = await readFile(filePath, "utf8");
  const relative = path.relative(repoRoot, filePath);

  if (!hasFrontmatter(text)) {
    report("WARN", relative, "missing YAML frontmatter");
  }

  for (const pattern of secretPatterns) {
    if (pattern.test(text)) {
      report("FAIL", relative, `matched sensitive pattern ${pattern}`);
      failures += 1;
    }
  }

  if (relative.includes("00_收件箱") && !text.includes("status:")) {
    report("FAIL", relative, "inbox note missing status frontmatter");
    failures += 1;
  }
}

if (failures > 0) {
  process.exitCode = 1;
} else {
  process.stdout.write(`validate-write: checked ${files.length} markdown file(s)\n`);
}

function hasFrontmatter(text) {
  return text.startsWith("---\n") && text.indexOf("\n---", 4) !== -1;
}

function report(level, filePath, message) {
  process.stderr.write(`${level}: ${filePath}: ${message}\n`);
}

async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}

async function collectMarkdown(root, limit) {
  const results = [];
  async function visit(dir) {
    if (results.length >= limit || !(await exists(dir))) return;
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (results.length >= limit) return;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await visit(fullPath);
      } else if (entry.name.endsWith(".md")) {
        results.push(fullPath);
      }
    }
  }
  await visit(root);
  return results;
}
