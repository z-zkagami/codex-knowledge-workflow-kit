---
name: llm-wiki
description: Use when a topic will accumulate sources over time and should be maintained as a persistent wiki workspace under 30_研究 instead of being re-explained from raw material each time
---

# llm-wiki

这是当前知识库里对 `llm-wiki-skill` 的本地桥接层。

## 何时使用

- 某个主题会持续进新来源
- 不想每次重新喂给 AI 原始资料
- 需要围绕同一主题持续长出综合判断、对比和问题清单
- 这个主题未来可能晋升到 `40_知识库/` 或进入 `60_内容中台/`

## 在当前库里的落点

- 主题入口：`30_研究/<主题>/00_索引.md`
- llm wiki 工作区：`30_研究/<主题>/llm-wiki/`
- 原始素材：`30_研究/<主题>/llm-wiki/raw/`
- AI wiki：`30_研究/<主题>/llm-wiki/wiki/`

## 目录角色

- `raw/`：原始来源，只读
- `wiki/`：AI 持续维护的主题 wiki
- `00_索引.md`：这个主题和主库之间的桥

## 工作流

### 1. 初始化

优先使用：

```bash
bash scripts/init_llm_wiki_workspace.sh "<主题名>"
```

这会在 `30_研究/<主题>/` 下创建入口文件，并在 `llm-wiki/` 里初始化 Karpathy 风格工作区。

### 2. 消化素材

进入该主题的 `llm-wiki/` 目录后，按上游 skill 的工作流执行：

- `init`
- `ingest`
- `batch-ingest`
- `query`
- `digest`
- `lint`
- `status`
- `graph`

## 和主知识库的关系

- `llm-wiki` 不是 `40_知识库/` 的替代
- 它是 `30_研究/` 内的主题工作台
- 只有成熟判断、稳定方法、可复用概念才晋升到 `40_知识库/`
- 有传播价值的内容进入 `60_内容中台/00_选题池/`

## 重要规则

- 不要把所有内容都塞进 llm wiki，只给长期跟踪主题使用
- `raw`、`wiki`、`正式知识` 的角色必须区分清楚
- 公开输出前重新检查隐私和工作敏感信息

## 参考

- 集成说明：`99_系统/配置/llm-wiki-集成.md`
- 本地安装后的上游 skill：`~/.codex/skills/llm-wiki/`
