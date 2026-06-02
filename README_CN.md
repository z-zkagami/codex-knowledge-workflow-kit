# Codex Knowledge Workflow Kit

这是 Kagami 维护的本地优先 AI Agent 持久化工作记忆层。

它把 Obsidian 风格 Markdown vault 变成可编辑、可搜索、可版本化的外部记忆底座，让 Codex、Claude Code、Gemini CLI 等 agent 能跨 session 记住目标、规则、项目、研究和输出链路。

## 三层架构

### Memory Layer

记忆层负责保存稳定上下文：

* `AGENTS.md`：项目规则和协作行为
* `99_系统/记忆/`：North Star、记忆、关键决策、模式、踩坑和 skills
* `_state/CURRENT.md`、`DECISIONS.md`、`HANDOFF.md`：项目和研究主题的连续状态
* `vault-manifest.json`：vault 结构、QMD index、必备文件和校验约定

### Workflow Layer

工作流层负责把输入推进到下一步：

* `daily-signals -> triage-inbox -> llm-wiki`
* `research -> parse-knowledge -> QMD`
* `wechat-material-intake -> topic -> style -> draft -> title`
* `archive`

### Retrieval Layer

检索层负责让记忆可召回：

* QMD 本地语义检索
* Qwen3 中文 embedding
* 相关主题发现
* 跨 session 上下文包

## 快速检查

初始化真实知识库，并安装 Codex adapter：

```bash
node scripts/init-kit.mjs --vault "$HOME/path/to/my-vault" --tool codex
```

安装全部内置 adapter：

```bash
node scripts/init-kit.mjs --vault "$HOME/path/to/my-vault" --tool all
```

```bash
bash scripts/check_cn_layout.sh
```

绑定真实知识库：

```bash
export CKW_VAULT_ROOT="$HOME/path/to/my-vault"
bash scripts/check_cn_layout.sh
```

预览 session 启动上下文：

```bash
node scripts/session-start.mjs
```

根据用户输入推荐工作流：

```bash
node scripts/classify-message.mjs "整理今天的 AI 信号"
```

按 prompt 注入相关 vault memory：

```bash
node scripts/memory-inject.mjs "agent workflow capture 长期研究"
```

校验 Markdown 写入：

```bash
node scripts/validate-write.mjs examples/demo-vault/00_收件箱/2026-06-02-agent-workflow-capture.md
```

查看完整记忆闭环：

```bash
open docs/demo-scenario.md
```

查看扩展方式：

```bash
open docs/extending.md
```

## 开源归属

本项目从既有 vault framework 演化而来，当前公开版聚焦 Kagami 的跨 AI 工具持久化工作记忆、Agent Skills、本地语义检索和内容流水线。原始来源见 `NOTICE.md`。
