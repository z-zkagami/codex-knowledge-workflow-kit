# X 内容提取使用指南

## 支持的 URL 格式

### 1. X Articles (长文章)
- 格式: `https://x.com/i/articles/[article_id]`
- 示例: `https://x.com/i/articles/1234567890`
- 特点: 完整的博客式长文，有标题和段落结构

### 2. 推文串 (Thread)
- 格式: `https://x.com/[username]/status/[tweet_id]`
- 示例: `https://x.com/elonmusk/status/1234567890`
- 特点: 多条连续推文组成的主题讨论

### 3. 单条推文
- 格式: `https://x.com/[username]/status/[tweet_id]`
- 示例: `https://x.com/user/status/9876543210`
- 特点: 独立的单条推文内容

## 提取流程

1. **获取 URL**: 用户提供 X 内容的链接
2. **提取内容**: 使用 MCP 工具或现有 skill 获取内容
3. **解析元数据**: 提取标题、作者、日期等信息
4. **格式化**: 转换为结构化的 Markdown 格式
5. **保存**: 使用脚本保存到指定目录

## Markdown 格式规范

```markdown
# [标题]

---
作者: [作者名]
原文链接: [URL]
发布时间: [YYYY-MM-DD HH:MM:SS]
提取时间: [YYYY-MM-DD HH:MM:SS]
---

[正文内容]
```

## 文件命名规则

- 优先使用内容标题作为文件名
- 移除特殊字符 `<>:"/\|?*`
- 限制长度不超过 100 字符
- 如无标题，使用时间戳: `x_content_YYYYMMDD_HHMMSS.md`
- 重名文件自动添加数字后缀: `filename_1.md`, `filename_2.md`

## 错误处理

- URL 无法访问: 提示用户检查链接有效性
- 内容为空: 提示可能是私密推文或已删除
- 保存失败: 检查目录权限和磁盘空间
