#!/usr/bin/env node

import { readFile } from "node:fs/promises";

async function readStdin() {
  if (process.stdin.isTTY) return "";
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

const argText = process.argv.slice(2).join(" ");
const stdinText = await readStdin();
let text = `${argText}\n${stdinText}`.trim();

try {
  const payload = JSON.parse(text);
  text = JSON.stringify(payload);
} catch {
  // Plain text input is expected during local testing.
}

const rules = [
  {
    workflow: "daily-signals",
    keywords: ["signal", "signals", "newsletter", "AI-HOT", "daily brief", "worth reading"],
    hint: "Build a daily signal brief and route high-value items.",
  },
  {
    workflow: "triage-inbox",
    keywords: ["Inbox", "inbox", "triage", "input", "material", "capture", "captured", "route", "routing"],
    hint: "Route pending captures into action, project, research, wiki, content, or archive.",
  },
  {
    workflow: "llm-wiki",
    keywords: ["long-running topic", "wiki", "persistent topic", "topic workspace"],
    hint: "Create or update a persistent topic workspace.",
  },
  {
    workflow: "research",
    keywords: ["research", "deep dive", "source", "sources", "analysis", "investigate"],
    hint: "Plan and execute a research pass.",
  },
  {
    workflow: "wechat-*",
    keywords: ["wechat", "article", "topic", "outline", "draft", "title", "style"],
    hint: "Use material intake, topic planning, style profiling, draft writing, or title generation.",
  },
  {
    workflow: "archive",
    keywords: ["Archive", "archive", "done", "complete", "cleanup", "close"],
    hint: "Move completed work out of active spaces.",
  },
];

const normalized = text.toLowerCase();
const matches = rules.filter((rule) =>
  rule.keywords.some((keyword) => normalized.includes(keyword.toLowerCase())),
);

const selected = matches.length ? matches : [{ workflow: "ask", hint: "Answer directly or inspect the vault before choosing a workflow." }];

process.stdout.write("# Workflow Hints\n\n");
for (const item of selected) {
  process.stdout.write(`- ${item.workflow}: ${item.hint}\n`);
}
