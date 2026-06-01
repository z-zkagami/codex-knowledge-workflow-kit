---
name: wechat-draft-writer
description: 公众号初稿写作技能。用于在选题和大纲已确认后，基于参考资料、语音底稿和文风 DNA 生成一版高保真初稿。适用于正文写作阶段，不负责选题、大纲和标题决策。
---

# Wechat Draft Writer

## Overview
在结构已确认的前提下，把参考资料和语音底稿转成符合作者文风的公众号初稿。

## Workflow
1. Require confirmed outline, reference materials, voice transcript draft, Style DNA card, and article goal.
2. 如果用户还没有个人 Style DNA，先调用 `wechat-style-profiler` 生成。
3. DNA 加载顺序：frontmatter 里 `style_dna` 指定的文件 → `50_资源/风格参考/default-author/style-dna.md` → `references/author-style-dna.md`。
4. 在开写前明确声明当前使用的 Style DNA 文件。
5. 如果存在最近已发布且反馈明显更好的样本，先做一次 `结果反馈回流`：把该样本与 1-2 篇近期普通样本对比，提炼 3-5 条“被数据验证有效的写法”。
6. 读取 `references/ai-role-boundaries.md`，明确本次写作中 AI 该做什么、不该做什么。
7. Digest source material, separating hard facts from personal 观点、原话和待验证信息。
8. 为每个 section 生成内部写作 brief，不对外输出新的大纲版本。
9. 按 section 写出 `Draft v1`，执行 `references/draft-dna-enforcement.md` 的硬约束。
10. 对 AI 无法填充的内容（第一手经历、价值判断、情绪细节），使用占位标记（见 `ai-role-boundaries.md`）。
11. 跑 `references/draft-quality-checklist.md` 四层自检（L1 硬性规则 → L2 风格一致性 → L3 内容质量 → L4 活人感终审）。
12. 返回初稿、文风贴合说明、风险点、质检报告和作者改写建议。

## Output Contract
1. `Style DNA In Use`
2. `Validated Levers In Use`（如果有结果反馈回流，列出本次优先使用的 3-5 条有效写法）
3. `Draft v1`
4. `Style Adherence Notes`
5. `DNA Compliance Report`（四层质检报告，格式见 `draft-quality-checklist.md`）
6. `Weak Sections And Fix Suggestions`
7. `Author Rewrite Suggestions`（标注哪些段落特别需要作者加入个人声音、真实细节或价值判断）
8. `Optional Alternative Lead`

## Guardrails
- Avoid inventing facts; mark any uncertain claim with `[待补充证据]`.
- Distinguish source types explicitly: `参考资料` facts vs `语音底稿` personal expression.
- Keep paragraph granularity suitable for WeChat mobile reading.
- Preserve the user's habitual rhetorical devices from the Style DNA card.
- If no personal Style DNA is provided, hand off to `wechat-style-profiler` first.
- Prefer loading DNA from frontmatter `style_dna` link or `风格画像-融合版.md`.
- `references/author-style-dna.md` and `style-dna-default-template.md` are fallbacks only, not for final publish drafts.
- Must explicitly tell the user which DNA file or author profile is being used before presenting the draft.
- Must read `references/ai-role-boundaries.md` before writing and respect the AI/human boundary throughout.
- Never fabricate first-hand experiences, personal judgments, or emotional details; use placeholder marks instead.
- If a recent published sample has clearly better feedback, prefer those validated levers over static stylistic habits when they conflict, but explain the tradeoff.
- Do not overfit to one high-performing sample; extract reusable levers, not one-off wording or accidental gimmicks.
- Keep paragraph length within 1-3 sentences unless explicitly requested.
- Do not use em dashes.
- If hard-fail pattern is detected, rewrite before returning output.
- If outline is not confirmed, hand off to `wechat-topic-outline-planner` instead of drafting.
- Quality check must pass all 4 layers (L1-L4) before delivering draft. If any layer fails, fix before output.
