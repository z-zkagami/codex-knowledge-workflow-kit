#!/usr/bin/env python3
"""
从 X (Twitter) 提取内容并保存为 Markdown 文件
支持：长文章 (X Articles)、推文串 (Thread)、单条推文
支持智能分类保存到不同主题文件夹
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

VAULT_ROOT = os.environ.get("CKW_VAULT_ROOT", os.path.join(os.getcwd(), "examples", "demo-vault"))

# 默认保存路径
DEFAULT_SAVE_PATH = os.environ.get("CKW_X_SAVE_PATH", os.path.join(VAULT_ROOT, "60_内容中台", "00_选题池"))

# X 素材分类库路径
MATERIAL_LIBRARY_BASE = os.environ.get("CKW_X_LIBRARY_PATH", os.path.join(DEFAULT_SAVE_PATH, "X文章库"))

# 支持的分类目录
CATEGORIES = {
    "skill": "Skill系列",
    "openclaw": "OpenClaw系列",
    "opencode": "OpenCode系列",
    "codex": "Codex系列",
    "claude": "Claude系列",
    "ai-tools": "AI工具系列",
    "unclassified": "待分类"
}

def sanitize_filename(title):
    """清理文件名，移除不允许的字符"""
    # 移除或替换不允许的字符
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    # 限制长度
    if len(title) > 100:
        title = title[:100]
    return title.strip()

def extract_metadata(content_data):
    """从内容数据中提取元数据"""
    metadata = {
        'title': content_data.get('title', ''),
        'author': content_data.get('author', ''),
        'url': content_data.get('url', ''),
        'date': content_data.get('date', ''),
        'type': content_data.get('type', 'unknown')  # article, thread, tweet
    }
    return metadata

def format_markdown(content, metadata):
    """格式化为 Markdown 内容"""
    md_lines = []

    # 添加标题
    if metadata['title']:
        md_lines.append(f"# {metadata['title']}\n")

    # 添加元数据
    md_lines.append("---")
    if metadata['author']:
        md_lines.append(f"作者: {metadata['author']}")
    if metadata['url']:
        md_lines.append(f"原文链接: {metadata['url']}")
    if metadata['date']:
        md_lines.append(f"发布时间: {metadata['date']}")
    md_lines.append(f"提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_lines.append("---\n")

    # 添加正文内容
    md_lines.append(content)

    return "\n".join(md_lines)

def save_markdown(content, metadata, save_path=None, category=None):
    """保存 Markdown 文件

    Args:
        content: Markdown 内容
        metadata: 文章元数据
        save_path: 自定义保存路径（优先级最高）
        category: 分类标识（openclaw/claude/ai-tools/unclassified）
    """
    # 确定保存路径（优先级：save_path > category > DEFAULT_SAVE_PATH）
    if save_path is None:
        if category and category in CATEGORIES:
            # 使用新系统的分类路径
            save_path = os.path.join(MATERIAL_LIBRARY_BASE, CATEGORIES[category])
        else:
            # 使用旧系统的默认路径
            save_path = DEFAULT_SAVE_PATH

    # 确保目录存在
    Path(save_path).mkdir(parents=True, exist_ok=True)

    # 生成文件名
    if metadata['title']:
        filename = sanitize_filename(metadata['title'])
    else:
        filename = f"x_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 添加 .md 扩展名
    filename = f"{filename}.md"

    # 完整路径
    full_path = os.path.join(save_path, filename)

    # 如果文件已存在，添加数字后缀
    counter = 1
    base_path = full_path
    while os.path.exists(full_path):
        name_without_ext = base_path[:-3]  # 移除 .md
        full_path = f"{name_without_ext}_{counter}.md"
        counter += 1

    # 保存文件
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return full_path

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 extract_x_content.py <markdown_content> [metadata_json] [--category=分类]")
        print("示例: python3 extract_x_content.py \"内容\" '{\"title\":\"标题\",\"author\":\"作者\"}' --category=openclaw")
        print("支持的分类: openclaw, claude, ai-tools, unclassified")
        sys.exit(1)

    # 获取内容
    markdown_content = sys.argv[1]

    # 获取元数据（如果提供）
    metadata = {
        'title': '',
        'author': '',
        'url': '',
        'date': '',
        'type': 'unknown'
    }

    if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
        try:
            metadata.update(json.loads(sys.argv[2]))
        except json.JSONDecodeError:
            print("警告: 元数据 JSON 格式错误，使用默认值")

    # 检查是否有分类参数
    category = None
    for arg in sys.argv[2:]:
        if arg.startswith('--category='):
            category = arg.split('=')[1]
            if category not in CATEGORIES:
                print(f"警告: 未知分类 '{category}'，将使用默认路径")
                category = None
            break

    # 格式化 Markdown
    formatted_content = format_markdown(markdown_content, metadata)

    # 保存文件
    saved_path = save_markdown(formatted_content, metadata, category=category)

    # 输出结果（包含分类信息）
    if category:
        print(f"✅ 内容已保存到: {saved_path}")
        print(f"📁 分类: {CATEGORIES[category]}")
    else:
        print(f"✅ 内容已保存到: {saved_path}")

    return saved_path

if __name__ == "__main__":
    main()
