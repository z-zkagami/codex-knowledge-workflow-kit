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
    keywords: ["信号", "newsletter", "AI-HOT", "日报", "今天值得看"],
    hint: "Build a daily signal brief and route high-value items.",
  },
  {
    workflow: "triage-inbox",
    keywords: ["收件箱", "inbox", "分诊", "整理输入", "处理素材"],
    hint: "Route pending captures into action, project, research, wiki, content, or archive.",
  },
  {
    workflow: "llm-wiki",
    keywords: ["长期主题", "wiki", "持续研究", "主题工作区"],
    hint: "Create or update a persistent topic workspace.",
  },
  {
    workflow: "research",
    keywords: ["研究", "调研", "deep dive", "资料", "分析"],
    hint: "Plan and execute a research pass.",
  },
  {
    workflow: "wechat-*",
    keywords: ["公众号", "选题", "大纲", "初稿", "标题", "文风"],
    hint: "Use material intake, topic planning, style profiling, draft writing, or title generation.",
  },
  {
    workflow: "archive",
    keywords: ["归档", "archive", "完成", "清理"],
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
