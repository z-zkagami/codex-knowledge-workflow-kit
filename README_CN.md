# Codex Knowledge Workflow Kit

这是 Kagami 维护的本地优先知识工作流包，用 Codex 和 Agent Skills 管理 Obsidian 风格知识库。

它把原始输入推进到项目、研究笔记、知识卡和可发布内容，并沉淀成可复用的脚本、模板和 skills。

## 核心能力

* 用 `AGENTS.md` 固化 Codex 协作规则
* 用 `daily-signals -> triage-inbox -> llm-wiki` 建立外部信号处理链路
* 用 `research -> parse-knowledge -> QMD` 建立研究和本地语义检索链路
* 用 `wechat-*` skills 建立内容生产链路
* 用脚本校验目录、抓取 RSS、同步 Flomo、刷新 QMD embedding、管理 Python 环境

## 快速检查

```bash
bash scripts/check_cn_layout.sh
```

绑定真实知识库：

```bash
export CKW_VAULT_ROOT="$HOME/path/to/my-vault"
bash scripts/check_cn_layout.sh
```

## 开源归属

本项目从既有 vault framework 演化而来，当前公开版聚焦 Kagami 的 Codex-native 工作流、Agent Skills、本地语义检索和内容流水线。原始来源见 `NOTICE.md`。
