# X Extractor Usage Guide

## URL Formats

- X Article: `https://x.com/i/articles/<article_id>`
- X post or thread root: `https://x.com/<username>/status/<tweet_id>`

## Markdown Format

```markdown
# Title

---
author: Author
source_url: https://x.com/user/status/123
published_at: 2026-06-02
extracted_at: 2026-06-02 10:00:00
content_type: tweet
---

Body content.
```

## File Naming

- Prefer the title as the filename.
- Remove unsupported filename characters.
- Use `x_content_YYYYMMDD_HHMMSS.md` when no title exists.
- Add numeric suffixes for collisions.

## Error Handling

- Invalid URL: ask the user for a valid X/Twitter link.
- Empty content: explain that the post may be private, deleted, or unavailable.
- Save failure: check the target directory and permissions.
