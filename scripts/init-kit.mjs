#!/usr/bin/env node

import { mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const manifestPath = path.join(repoRoot, "vault-manifest.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const args = parseArgs(process.argv.slice(2));

if (args.help) {
  printUsage();
  process.exit(0);
}

const availableAdapters = await listAdapters();

if (args.listTools) {
  for (const adapter of availableAdapters) {
    process.stdout.write(`${adapter.name}\t${adapter.displayName}\t${adapter.description}\n`);
  }
  process.exit(0);
}

const vaultRoot = args.vault || process.env.CKW_VAULT_ROOT;
if (!vaultRoot) {
  printUsage();
  process.stderr.write("\nERROR: provide --vault <path> or set CKW_VAULT_ROOT.\n");
  process.exit(1);
}

const selectedTools = selectTools(args.tool || "codex", availableAdapters);
const targetRoot = path.resolve(vaultRoot);
const dryRun = Boolean(args.dryRun);
const force = Boolean(args.force);
const operations = [];

await ensureDirectory(targetRoot);
await createVaultStructure(targetRoot);
await writeVaultManifest(targetRoot);
await installAdapters(targetRoot, selectedTools);

process.stdout.write("# Init Summary\n\n");
process.stdout.write(`Vault: ${targetRoot}\n`);
process.stdout.write(`Kit root: ${repoRoot}\n`);
process.stdout.write(`Tools: ${selectedTools.map((tool) => tool.name).join(", ")}\n`);
process.stdout.write(`Mode: ${dryRun ? "dry-run" : "write"}${force ? " + force" : ""}\n\n`);
for (const operation of operations) {
  process.stdout.write(`- ${operation}\n`);
}
process.stdout.write("\nNext commands:\n\n");
process.stdout.write(`export CKW_KIT_ROOT="${repoRoot}"\n`);
process.stdout.write(`export CKW_VAULT_ROOT="${targetRoot}"\n`);
process.stdout.write("node \"$CKW_KIT_ROOT/scripts/session-start.mjs\"\n");
process.stdout.write("node \"$CKW_KIT_ROOT/scripts/memory-inject.mjs\" \"agent workflow capture 长期研究\"\n");
process.stdout.write("bash \"$CKW_KIT_ROOT/scripts/check_cn_layout.sh\"\n");

function parseArgs(items) {
  const parsed = {};
  for (let index = 0; index < items.length; index += 1) {
    const item = items[index];
    if (item === "--help" || item === "-h") parsed.help = true;
    else if (item === "--dry-run") parsed.dryRun = true;
    else if (item === "--force") parsed.force = true;
    else if (item === "--list-tools") parsed.listTools = true;
    else if (item === "--vault") parsed.vault = items[++index];
    else if (item === "--tool") parsed.tool = items[++index];
    else {
      process.stderr.write(`Unknown argument: ${item}\n`);
      parsed.help = true;
    }
  }
  return parsed;
}

function printUsage() {
  process.stdout.write(`Usage:
  node scripts/init-kit.mjs --vault <path> [--tool codex|claude-code|gemini-cli|cursor|all]

Options:
  --vault <path>    Target Obsidian-style vault path.
  --tool <name>     Tool adapter to install. Default: codex.
  --dry-run         Print planned operations without writing files.
  --force           Overwrite existing generated files.
  --list-tools      List available adapters.
  --help            Show this message.

Examples:
  node scripts/init-kit.mjs --vault "$HOME/Vault" --tool codex
  node scripts/init-kit.mjs --vault "$HOME/Vault" --tool all --dry-run
`);
}

async function listAdapters() {
  const adaptersRoot = path.join(repoRoot, "adapters");
  const entries = await readdir(adaptersRoot, { withFileTypes: true });
  const adapters = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const adapterRoot = path.join(adaptersRoot, entry.name);
    const configPath = path.join(adapterRoot, "adapter.json");
    const config = JSON.parse(await readFile(configPath, "utf8"));
    adapters.push({ ...config, root: adapterRoot });
  }
  return adapters.sort((a, b) => a.name.localeCompare(b.name));
}

function selectTools(toolName, adapters) {
  if (toolName === "all") return adapters;
  const adapter = adapters.find((item) => item.name === toolName);
  if (!adapter) {
    process.stderr.write(`Unknown tool adapter: ${toolName}\n`);
    process.stderr.write(`Available: ${adapters.map((item) => item.name).join(", ")}, all\n`);
    process.exit(1);
  }
  return [adapter];
}

async function createVaultStructure(root) {
  for (const rootPath of Object.values(manifest.roots)) {
    await ensureDirectory(path.join(root, rootPath));
  }

  for (const filePath of manifest.memoryFiles) {
    await writeIfMissing(path.join(root, filePath), memoryContent(filePath));
  }

  await createResourceStructure(root);
  await createContentStructure(root);

  await writeIfMissing(
    path.join(root, "00_收件箱", "README.md"),
    frontmatter("docs", "active", ["inbox"]) +
      "# Inbox\n\nCapture raw inputs here, then route them with `triage-inbox`.\n",
  );
}

async function writeVaultManifest(root) {
  const target = path.join(root, "vault-manifest.json");
  const content = `${JSON.stringify(manifest, null, 2)}\n`;
  await writeIfMissing(target, content);
}

async function createResourceStructure(root) {
  const resourcesRoot = path.join(root, "50_资源");
  for (const dirName of ["Newsletters", "信号简报", "风格参考", "临时收纳"]) {
    await ensureDirectory(path.join(resourcesRoot, dirName));
  }
  await writeIfMissing(
    path.join(resourcesRoot, "00_资源工作台.md"),
    frontmatter("resources-workbench", "active", ["resources"]) +
      "# Resources Workbench\n\n## Active Feeds\n\n- AI HOT RSS\n- Manual article captures\n- Video transcripts\n\n## Review Cadence\n\n- Daily: signal brief\n- Weekly: promote durable findings into research or wiki\n",
  );
}

async function createContentStructure(root) {
  await ensureDirectory(path.join(root, "60_内容中台", "10_公众号"));
  await ensureDirectory(path.join(root, "60_内容中台", "20_小红书", "素材池"));
}

async function installAdapters(root, adapters) {
  for (const adapter of adapters) {
    for (const file of adapter.files) {
      const source = path.join(adapter.root, file.source);
      const target = path.join(root, file.target);
      await copyIfMissing(source, target);
    }
  }
}

function memoryContent(filePath) {
  const title = path.basename(filePath, ".md");
  const bodyByTitle = {
    "North Star": "This vault is a persistent memory layer for AI agents.\n\nUse it to preserve goals, rules, projects, research state, decisions, patterns, gotchas, and output workflows across sessions.\n",
    Memories: "Add stable cross-session facts here after they prove useful more than once.\n",
    "Key Decisions": "Record decisions that should shape future work.\n",
    Patterns: "Record repeatable workflows and habits that help agents work better in this vault.\n",
    Gotchas: "Record failure modes, privacy boundaries, and checks that prevent repeated mistakes.\n",
    Skills: "Record installed workflow packs and routing notes.\n",
  };
  return `${frontmatter("memory", "active", ["memory"])}# ${title}\n\n${bodyByTitle[title] ?? ""}`;
}

function frontmatter(type, status, tags) {
  return `---\ntype: ${type}\ncreated: ${today()}\nstatus: ${status}\ntags:\n${tags.map((tag) => `  - ${tag}`).join("\n")}\n---\n`;
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

async function copyIfMissing(source, target) {
  const content = await readFile(source, "utf8");
  await writeIfMissing(target, content);
}

async function writeIfMissing(filePath, content) {
  await ensureDirectory(path.dirname(filePath));
  const existsAlready = await exists(filePath);
  if (existsAlready && !force) {
    operations.push(`skip existing ${displayPath(filePath)}`);
    return;
  }
  operations.push(`${existsAlready ? "overwrite" : "create"} ${displayPath(filePath)}`);
  if (!dryRun) await writeFile(filePath, content, "utf8");
}

async function ensureDirectory(dirPath) {
  if (!dryRun) await mkdir(dirPath, { recursive: true });
}

function displayPath(filePath) {
  const normalized = path.resolve(filePath);
  if (normalized === targetRoot) return "<vault>";
  if (normalized.startsWith(`${targetRoot}${path.sep}`)) {
    return `<vault>/${path.relative(targetRoot, normalized)}`;
  }
  if (normalized.startsWith(`${repoRoot}${path.sep}`)) {
    return path.relative(repoRoot, normalized);
  }
  return normalized;
}

async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}
