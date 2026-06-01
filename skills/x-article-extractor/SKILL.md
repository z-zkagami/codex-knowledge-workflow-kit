---
name: x-article-extractor X文章提取器
description: 从 X (Twitter) 提取内容（长文章、推文串、单条推文）并保存为本地 Markdown 文件。支持智能分类保存到对应主题文件夹，并自动更新素材索引。当用户提供 X 链接并要求提取、保存或转换为 Markdown 时使用此 skill。
---

# X 内容提取器（智能分类版）

## 功能说明

从 X (Twitter) 提取各类内容并保存为结构化的 Markdown 文件到本地，支持长文章 (X Articles)、推文串 (Thread) 和单条推文。

**新功能**：
- ✅ **智能主题分类**：AI 自动分析文章主题，保存到对应分类文件夹
- ✅ **自动更新素材索引**：提取关键词，更新素材速查表
- ✅ **无缝集成内容生产系统**：直接保存到新的素材库目录结构

## Script Directory

Scripts located in `scripts/` subdirectory.

**Path Resolution**:
1. `SKILL_DIR` = this SKILL.md's directory
2. Script path = `${SKILL_DIR}/scripts/extract_x_content.py`

**Usage**:
```bash
python3 ${SKILL_DIR}/scripts/extract_x_content.py "<content>" '<metadata>'
```

## 使用时机

当用户提出以下需求时使用此 skill：

- "把这个 X 文章提取成 Markdown"
- "保存这条推文到本地"
- "下载这个推文串"
- "从 X 上提取内容"
- 提供 X/Twitter 链接并要求保存或转换

## 工作流程

### 1. 获取内容

**优先选项 A - 使用 baoyu-danger-x-to-markdown skill**（推荐）:

调用 `baoyu-danger-x-to-markdown` skill 提取内容（需要用户同意使用逆向 API）。

该 skill 会：
- 自动打开 Chrome 浏览器
- 引导用户在浏览器中登录 X 账号（如果未登录）
- 获取登录凭证（cookies）
- 通过逆向工程的 API 提取推文内容
- 支持长文章 (X Articles)、推文串 (Thread) 和单条推文

**重要提示**：
- 首次使用需要在打开的 Chrome 窗口中登录 X 账号
- 登录凭证会被缓存，后续使用无需重复登录
- 此方法使用逆向 API，需要用户同意免责声明

**备选选项 B - 使用 MCP 工具**（如果可用且未超额）:
```
mcp__web-reader__webReader
```
参数：
- `url`: X 内容的 URL
- `return_format`: "markdown"
- `retain_images`: true（保留图片引用）

注：MCP 工具有月度使用限额

### 2. 解析内容和元数据

从获取的内容中提取：
- **标题**: 长文章的标题，或推文的前 50 字符
- **作者**: 用户名/显示名
- **URL**: 原始链接
- **发布时间**: 推文/文章的发布时间
- **类型**: article/thread/tweet

提示：
- 长文章通常有明确的标题字段
- 推文串使用第一条推文内容作为标题
- 单条推文使用内容前 50 字符作为标题

### 2.5 智能主题分类（新增）

**在保存前，AI 自动分析文章主题，判断分类：**

1. **分析内容关键词**：
   - 查看标题、正文内容
   - 提取核心主题关键词

2. **判断分类**（按优先级从高到低）：

   - **Skill系列** (`skill`)：【优先级最高】
     - 关键词包含：skill 开发, skill 创建, skill-creator, 自定义 skill, skill 教程, skill 使用
     - 示例：如何创建 skill、skill 开发技巧、skill 最佳实践
     - **注意**：只要涉及 skill 开发/使用，优先归到此类

   - **OpenClaw系列** (`openclaw`)：
     - 关键词包含：OpenClaw, Claw, agent 工作流, .clauderules, hooks, MCP server
     - 但**不涉及** skill 开发（skill 开发优先归到 Skill系列）
     - 示例：OpenClaw 配置教程、agent 协作、hooks 使用

   - **OpenCode系列** (`opencode`)：
     - 关键词包含：OpenCode, cursor, windsurf, 代码编辑器, IDE, 编程工具
     - 示例：OpenCode 使用技巧、cursor 配置、windsurf 教程

   - **Codex系列** (`codex`)：
     - 关键词包含：Codex, AI 编程助手, 代码生成, 编程 AI
     - 示例：Codex 使用技巧、AI 编程实践

   - **Claude系列** (`claude`)：
     - 关键词包含：Claude Code, Claude API, 提示词, prompt, 技巧, 工作流, tips
     - 但**不涉及** skill 开发、OpenClaw、OpenCode、Codex
     - 示例：Claude Code 使用技巧、提示词优化、Claude API 教程

   - **AI工具系列** (`ai-tools`)：
     - 关键词包含：AI 工具, 写作, 视频, 图像生成, 自动化, workflow
     - 但**不是** Claude/OpenClaw/OpenCode/Skill/Codex 专属
     - 示例：AI 写作工具、视频剪辑工具、图像生成工具

   - **待分类** (`unclassified`)：
     - 无法明确判断，或主题混合
     - 稍后人工整理

3. **确定分类参数**：
   - 根据判断结果，确定 `--category` 参数值
   - 如果不确定，使用 `unclassified`
   - **优先级**：skill > openclaw/opencode/codex > claude > ai-tools > unclassified

### 3. 格式化并保存（支持智能分类）

使用 skill 目录下的 `scripts/extract_x_content.py` 脚本格式化并保存内容。

**脚本用法（新版）**:
```bash
python3 ${SKILL_DIR}/scripts/extract_x_content.py "<markdown_content>" '<metadata_json>' --category=<分类>
```

**参数说明**:
- `<markdown_content>`: 提取的 Markdown 内容（必需）
- `<metadata_json>`: JSON 格式的元数据（可选），包含：
  ```json
  {
    "title": "文章标题",
    "author": "作者名",
    "url": "原文链接",
    "date": "发布时间",
    "type": "article/thread/tweet"
  }
  ```
- `--category=<分类>`: 分类参数（新增，可选），支持的值：
  - `skill`: Skill系列（最高优先级）
  - `openclaw`: OpenClaw系列
  - `opencode`: OpenCode系列
  - `codex`: Codex系列
  - `claude`: Claude系列
  - `ai-tools`: AI工具系列
  - `unclassified`: 待分类
  - 如不指定，默认保存到 `CKW_X_SAVE_PATH` 或当前仓库的 demo vault 选题池

**示例**:
```bash
# 分类为 Skill系列（优先级最高）
python3 ${SKILL_DIR}/scripts/extract_x_content.py "这是推文内容..." '{"title":"如何创建自定义 Skill","author":"用户名","url":"https://x.com/user/status/123","date":"2024-01-20","type":"article"}' --category=skill

# 分类为 OpenClaw系列
python3 ${SKILL_DIR}/scripts/extract_x_content.py "这是推文内容..." '{"title":"OpenClaw Agent 工作流","author":"用户名","url":"https://x.com/user/status/456","date":"2024-01-21","type":"article"}' --category=openclaw

# 分类为 OpenCode系列
python3 ${SKILL_DIR}/scripts/extract_x_content.py "这是推文内容..." '{"title":"Cursor 使用技巧","author":"用户名","url":"https://x.com/user/status/789","date":"2024-01-22","type":"tweet"}' --category=opencode

# 分类为 Codex系列
python3 ${SKILL_DIR}/scripts/extract_x_content.py "这是推文内容..." '{"title":"Codex AI 编程实践","author":"用户名","url":"https://x.com/user/status/222","date":"2024-01-24","type":"article"}' --category=codex

# 分类为 Claude系列
python3 ${SKILL_DIR}/scripts/extract_x_content.py "这是推文内容..." '{"title":"Claude Code 10个技巧","author":"用户名","url":"https://x.com/user/status/111","date":"2024-01-23","type":"article"}' --category=claude
```

### 4. 保存位置（智能分类）

**新系统（推荐）**：根据分类参数保存到对应文件夹，默认根目录为 `CKW_X_LIBRARY_PATH`
```
<CKW_X_LIBRARY_PATH>/
├── Skill系列/              (--category=skill) 【优先级最高】
├── OpenClaw系列/           (--category=openclaw)
├── OpenCode系列/           (--category=opencode)
├── Codex系列/              (--category=codex)
├── Claude系列/             (--category=claude)
├── AI工具系列/             (--category=ai-tools)
└── 待分类/                 (--category=unclassified)
```

**默认路径**：如果不指定 `--category` 参数
```
<CKW_X_SAVE_PATH>
```

**文件命名规则**：
- 使用内容标题作为文件名（自动清理特殊字符）
- 如无标题，使用时间戳格式: `x_content_YYYYMMDD_HHMMSS.md`
- 重名文件自动添加数字后缀

### 5. 更新素材索引（新增）

**保存成功后，自动更新素材索引**：

1. **读取素材索引文件**：
   `<CKW_X_LIBRARY_PATH>/../素材索引.md`

2. **更新内容**：
   - 在 "主题分类速查" 下增加文章条目
   - 在 "关键词索引" 下添加关键词映射
   - 更新统计数据（文章总数）

3. **示例更新**：
   ```markdown
   ## 📁 主题分类速查

   ### Skill系列 (5篇)
   - 如何创建自定义 Skill.md - skill 创建、开发、教程
   - Skill Creator 最佳实践.md - skill 开发、技巧
   - ... (新增的文章)

   ### OpenClaw系列 (3篇)
   - Agent 训练师进阶指南.md - Discord、OpenClaw 协作
   - OpenClaw Hooks 使用指南.md - hooks、自动化
   - ... (新增的文章)

   ### OpenCode系列 (2篇)
   - Cursor 使用技巧.md - cursor、IDE
   - ... (新增的文章)

   ### Codex系列 (1篇)
   - Codex AI 编程实践.md - codex、代码生成
   - ... (新增的文章)

   ## 🔍 关键词索引

   - "skill 开发" → Skill系列/如何创建自定义 Skill.md
   - "skill creator" → Skill系列/Skill Creator 最佳实践.md
   - "hooks" → OpenClaw系列/OpenClaw Hooks 使用指南.md
   - "cursor" → OpenCode系列/Cursor 使用技巧.md
   - "codex" → Codex系列/Codex AI 编程实践.md
   - ... (新增的关键词)
   ```

### 6. 确认完成

向用户报告：
- ✅ 提取成功
- 📁 分类信息（如：OpenClaw系列）
- 📄 文件保存路径
- 📊 内容类型和基本信息（字数、作者等）
- 🔍 已更新素材索引

## 详细参考

需要了解更多细节时，读取 `references/usage_guide.md`，包含：
- 支持的 URL 格式详解
- Markdown 格式规范
- 错误处理指南

## 注意事项

1. **权限**: 私密推文或受保护账号的内容可能无法访问
2. **已删除内容**: 已删除的推文无法提取
3. **图片处理**: 图片会以链接形式保留在 Markdown 中（不下载原图）
4. **文件冲突**: 同名文件会自动添加数字后缀，不会覆盖

## 错误处理

- **URL 无效**: 提示用户检查链接格式
- **内容为空**: 说明可能是私密/已删除内容
- **保存失败**: 检查目录权限（脚本会自动创建目录）
