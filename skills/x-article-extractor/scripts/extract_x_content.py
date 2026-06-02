#!/usr/bin/env python3
"""Format extracted X/Twitter content and save it as Markdown."""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VAULT_ROOT = os.environ.get("CKW_VAULT_ROOT", os.path.join(os.getcwd(), "examples", "demo-vault"))
DEFAULT_SAVE_PATH = os.environ.get("CKW_X_SAVE_PATH", os.path.join(VAULT_ROOT, "60_Content", "00_Topic_Pool"))
MATERIAL_LIBRARY_BASE = os.environ.get("CKW_X_LIBRARY_PATH", os.path.join(DEFAULT_SAVE_PATH, "x-library"))

CATEGORIES = {
    "skill": "skill",
    "openclaw": "openclaw",
    "opencode": "opencode",
    "codex": "codex",
    "claude": "claude",
    "ai-tools": "ai-tools",
    "unclassified": "unclassified",
}


def sanitize_filename(title):
    """Remove unsupported filename characters and cap length."""
    title = re.sub(r'[<>:"/\\|?*]', "", title)
    if len(title) > 100:
        title = title[:100]
    return title.strip() or f"x_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def format_markdown(content, metadata):
    """Format extracted content as Markdown with YAML frontmatter."""
    title = metadata.get("title", "").strip()
    lines = []
    if title:
        lines.append(f"# {title}\n")

    lines.append("---")
    if metadata.get("author"):
        lines.append(f"author: {metadata['author']}")
    if metadata.get("url"):
        lines.append(f"source_url: {metadata['url']}")
    if metadata.get("date"):
        lines.append(f"published_at: {metadata['date']}")
    lines.append(f"extracted_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"content_type: {metadata.get('type', 'unknown')}")
    lines.append("---\n")
    lines.append(content)
    return "\n".join(lines)


def save_markdown(content, metadata, save_path=None, category=None):
    """Save Markdown content and avoid overwriting existing files."""
    if save_path is None:
        if category and category in CATEGORIES:
            save_path = os.path.join(MATERIAL_LIBRARY_BASE, CATEGORIES[category])
        else:
            save_path = DEFAULT_SAVE_PATH

    Path(save_path).mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(metadata.get("title") or "") + ".md"
    full_path = os.path.join(save_path, filename)

    counter = 1
    base_path = full_path
    while os.path.exists(full_path):
        name_without_ext = base_path[:-3]
        full_path = f"{name_without_ext}_{counter}.md"
        counter += 1

    with open(full_path, "w", encoding="utf-8") as handle:
        handle.write(content)

    return full_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_x_content.py <markdown_content> [metadata_json] [--category=<category>]")
        print('Example: python3 extract_x_content.py "content" \'{"title":"Title","author":"Author"}\' --category=codex')
        print("Categories: skill, openclaw, opencode, codex, claude, ai-tools, unclassified")
        sys.exit(1)

    markdown_content = sys.argv[1]
    metadata = {"title": "", "author": "", "url": "", "date": "", "type": "unknown"}

    if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
        try:
            metadata.update(json.loads(sys.argv[2]))
        except json.JSONDecodeError:
            print("Warning: metadata JSON is invalid; using defaults")

    category = None
    for arg in sys.argv[2:]:
        if arg.startswith("--category="):
            category = arg.split("=", 1)[1]
            if category not in CATEGORIES:
                print(f"Warning: unknown category '{category}'; using default path")
                category = None
            break

    formatted_content = format_markdown(markdown_content, metadata)
    saved_path = save_markdown(formatted_content, metadata, category=category)

    print(f"saved={saved_path}")
    if category:
        print(f"category={CATEGORIES[category]}")
    return saved_path


if __name__ == "__main__":
    main()
