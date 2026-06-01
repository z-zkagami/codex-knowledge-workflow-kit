#!/usr/bin/env python3

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


FLOMO_SECRET = os.environ.get("FLOMO_SECRET", "")
FLOMO_API_BASE = "https://flomoapp.com/api/v1"
DEFAULT_CONFIG_PATH = (
    Path.home()
    / "Library/Containers/com.flomoapp.m/Data/Library/Application Support/flomo/config.json"
)


class _FlomoHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.blocks: List[str] = []
        self._paragraph_chunks: List[str] = []
        self._list_chunks: List[str] = []
        self._current_link: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "p":
            self._flush_paragraph()
        elif tag == "br":
            self._append_text("\n")
        elif tag == "li":
            self._list_chunks.append("- ")
        elif tag == "a":
            self._current_link = attrs_dict.get("href")
        elif tag == "img":
            src = attrs_dict.get("src")
            alt = attrs_dict.get("alt") or "image"
            if src:
                self._append_text(f"![{alt}]({src})")

    def handle_endtag(self, tag: str) -> None:
        if tag == "p":
            self._flush_paragraph()
        elif tag == "li":
            item = "".join(self._list_chunks).strip()
            if item:
                self.blocks.append(item)
            self._list_chunks = []
        elif tag == "a":
            self._current_link = None

    def handle_data(self, data: str) -> None:
        text = html.unescape(data)
        self._append_text(text)

    def _append_text(self, text: str) -> None:
        if not text:
            return
        if self._current_link and text.strip():
            text = f"[{text}]({self._current_link})"
            self._current_link = None
        if self._list_chunks:
            self._list_chunks.append(text)
        else:
            self._paragraph_chunks.append(text)

    def _flush_paragraph(self) -> None:
        if not self._paragraph_chunks:
            return
        paragraph = "".join(self._paragraph_chunks)
        paragraph = re.sub(r"[ \t]+\n", "\n", paragraph)
        paragraph = re.sub(r"\n{3,}", "\n\n", paragraph)
        paragraph = "\n".join(line.rstrip() for line in paragraph.splitlines())
        paragraph = paragraph.strip()
        if paragraph:
            self.blocks.append(paragraph)
        self._paragraph_chunks = []


def html_to_markdown(raw_html: str) -> str:
    parser = _FlomoHtmlParser()
    parser.feed(raw_html or "")
    parser._flush_paragraph()
    blocks = [block.strip() for block in parser.blocks if block.strip()]
    if not blocks:
        return ""

    output: List[str] = [blocks[0]]
    previous_block = blocks[0]
    for block in blocks[1:]:
        if previous_block.startswith("- ") and block.startswith("- "):
            output.append("\n" + block)
        else:
            output.append("\n\n" + block)
        previous_block = block
    return "".join(output)


def strip_hashtag_prefix(line: str) -> str:
    cleaned = re.sub(r"^(?:#[^\s#]+(?:\s+|$))+", "", line).strip()
    return cleaned


def derive_title(markdown_text: str, tags: Iterable[str], slug: str) -> str:
    lines = [line.strip() for line in markdown_text.splitlines() if line.strip()]
    for line in lines:
        candidate = strip_hashtag_prefix(line)
        candidate = candidate.lstrip("- ").strip()
        if candidate:
            return candidate[:80]
    tags = [tag.strip() for tag in tags if tag.strip()]
    if tags:
        return f"{tags[0]} 记录"
    return f"flomo memo {slug}"


def infer_source_type(markdown_text: str) -> str:
    plain = re.sub(r"^#[^\n]+$", "", markdown_text, flags=re.MULTILINE).strip()
    non_empty = [line.strip() for line in plain.splitlines() if line.strip()]
    if len(non_empty) <= 2 and len(" ".join(non_empty)) <= 80:
        return "idea"
    return "note"


def infer_signal_type(source_type: str) -> str:
    return "灵感" if source_type == "idea" else "记录"


def sanitize_filename_component(value: str, max_length: int = 32) -> str:
    value = re.sub(r'[\\/:*?"<>|]+', "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.rstrip(".")
    return value[:max_length] or "untitled"


def build_note_filename(created_date: str, title: str, slug: str) -> str:
    safe_title = sanitize_filename_component(title, max_length=32)
    return f"{created_date}-flomo-{safe_title}-{slug}.md"


def parse_flomo_datetime(text: str) -> dt.datetime:
    return dt.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")


def to_unix_timestamp(text: str) -> int:
    local_tz = dt.datetime.now().astimezone().tzinfo
    parsed = parse_flomo_datetime(text)
    if local_tz is not None:
        parsed = parsed.replace(tzinfo=local_tz)
        return int(parsed.timestamp())
    return int(time.mktime(parsed.timetuple()))


def current_tz_offset_string() -> str:
    offset = dt.datetime.now().astimezone().utcoffset() or dt.timedelta()
    total_minutes = int(offset.total_seconds() // 60)
    sign = "-" if total_minutes < 0 else ""
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    return f"{sign}{hours}:{minutes}"


def format_frontmatter_scalar(value: str) -> str:
    if value == "":
        return ""
    if (
        "\n" not in value
        and '"' not in value
        and not re.search(r":\s", value)
        and not value.startswith(tuple("-?:!&*#{}[],|>%@`"))
        and value.lower() not in {"null", "true", "false", "yes", "no"}
    ):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_note(memo: Dict[str, object]) -> str:
    markdown_text = html_to_markdown(str(memo.get("content") or ""))
    tags = [str(tag) for tag in memo.get("tags") or []]
    slug = str(memo.get("slug") or "")
    created_at = str(memo.get("created_at") or "")
    updated_at = str(memo.get("updated_at") or "")
    created_date = created_at.split(" ", 1)[0] if created_at else ""
    deleted = bool(memo.get("deleted_at"))
    title = derive_title(markdown_text, tags, slug)
    source_type = infer_source_type(markdown_text)
    signal_type = infer_signal_type(source_type)
    topic = " / ".join(tags[:2])
    note_tags = ["inbox", "flomo", *tags]
    deduped_tags = list(dict.fromkeys(tag for tag in note_tags if tag))
    attachments = memo.get("files") or []

    lines = [
        "---",
        "type: inbox",
        f"created: {created_date}",
        f"title: {format_frontmatter_scalar(title)}",
        f"source_type: {source_type}",
        f"signal_type: {signal_type}",
        f"topic: {format_frontmatter_scalar(topic) if topic else ''}",
        "due:",
        "priority: B",
        "status: pending",
        f"source: flomo://memo/{slug}",
        "privacy: internal",
        "actionability: medium",
        "recommended_destination:",
        "next_step: 运行 `triage-inbox` 进行分诊",
        "related:",
        "tags:",
    ]
    for tag in deduped_tags:
        lines.append(f"  - {tag}")
    if deleted:
        lines.append("flomo_deleted: true")
    lines.extend(
        [
            "---",
            "",
            f"# {title}",
            "",
            "## 原始输入",
            "",
            markdown_text or "（空白 memo）",
            "",
            "## 捕获元数据",
            "",
            f"- flomo slug: `{slug}`",
            f"- 创建时间: `{created_at}`",
            f"- 最近更新: `{updated_at}`",
            f"- 采集来源: `{memo.get('source') or 'unknown'}`",
        ]
    )
    if attachments:
        lines.extend(["", "## 附件", ""])
        for index, file_info in enumerate(attachments, start=1):
            url = ""
            if isinstance(file_info, dict):
                url = str(file_info.get("url") or file_info.get("thumbnail_url") or "")
            if url:
                lines.append(f"- [附件 {index}]({url})")
    if deleted:
        lines.extend(
            [
                "",
                "## 删除状态",
                "",
                "该 memo 已在 flomo 中删除，当前仅保留这份收件箱副本以便后续人工判断是否归档。",
            ]
        )
    lines.append("")
    return "\n".join(lines)


@dataclasses.dataclass
class SyncState:
    path: Path
    cursor_updated_at: Optional[str] = None
    cursor_slug: str = ""
    memo_paths: Dict[str, str] = dataclasses.field(default_factory=dict)
    last_synced_at: Optional[str] = None

    @classmethod
    def load(cls, path: Path) -> "SyncState":
        if not path.exists():
            return cls(path=path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            path=path,
            cursor_updated_at=data.get("cursor_updated_at"),
            cursor_slug=data.get("cursor_slug", ""),
            memo_paths=dict(data.get("memo_paths", {})),
            last_synced_at=data.get("last_synced_at"),
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "cursor_updated_at": self.cursor_updated_at,
            "cursor_slug": self.cursor_slug,
            "memo_paths": self.memo_paths,
            "last_synced_at": self.last_synced_at,
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def load_flomo_config(config_path: Path) -> Dict[str, object]:
    return json.loads(config_path.read_text(encoding="utf-8"))


def build_signed_params(
    config: Dict[str, object],
    latest_updated_at: int,
    latest_slug: str,
    limit: int,
) -> Dict[str, object]:
    if not FLOMO_SECRET:
        raise RuntimeError("请先设置 FLOMO_SECRET 环境变量。")
    app_config = config.get("appConfig") or {}
    params = {
        "limit": limit,
        "latest_updated_at": latest_updated_at,
        "latest_slug": latest_slug,
        "tz": current_tz_offset_string(),
        "timestamp": int(time.time()),
        "api_key": "flomo_web",
        "app_version": app_config.get("VUE_APP_VERSION") or "5.0.0",
        "platform": "mac",
        "webp": "1",
    }
    raw = "&".join(
        f"{key}={params[key]}"
        for key in sorted(params)
        if params[key] or params[key] == 0
    )
    params["sign"] = hashlib.md5((raw + FLOMO_SECRET).encode("utf-8")).hexdigest()
    return params


def fetch_updated_memos(
    config: Dict[str, object],
    latest_updated_at: int,
    latest_slug: str,
    limit: int = 200,
) -> List[Dict[str, object]]:
    user = config.get("user") or {}
    access_token = user.get("access_token")
    if not access_token:
        raise RuntimeError("无法从 flomo 配置中读取 access_token。")

    params = build_signed_params(config, latest_updated_at, latest_slug, limit)
    url = f"{FLOMO_API_BASE}/memo/updated/?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("code") not in (0, None):
        raise RuntimeError(f"flomo API 返回异常: {payload.get('message')}")
    return list(payload.get("data") or [])


def choose_note_path(
    memo: Dict[str, object],
    inbox_dir: Path,
    state: SyncState,
) -> Path:
    slug = str(memo.get("slug") or "")
    existing = state.memo_paths.get(slug)
    if existing:
        path = Path(existing)
        if not path.is_absolute():
            return inbox_dir.parent / path
        return path

    created_date = str(memo.get("created_at") or "").split(" ", 1)[0]
    markdown_text = html_to_markdown(str(memo.get("content") or ""))
    title = derive_title(markdown_text, memo.get("tags") or [], slug)
    filename = build_note_filename(created_date, title, slug)
    return inbox_dir / filename


def relative_state_path(target: Path, vault_root: Path) -> str:
    try:
        return str(target.relative_to(vault_root))
    except ValueError:
        return str(target)


def sync_single_memo(
    memo: Dict[str, object],
    inbox_dir: Path,
    vault_root: Path,
    state: SyncState,
    dry_run: bool,
) -> Optional[Path]:
    slug = str(memo.get("slug") or "")
    path = choose_note_path(memo, inbox_dir, state)
    deleted = bool(memo.get("deleted_at"))

    if deleted and slug not in state.memo_paths:
        return None

    path.parent.mkdir(parents=True, exist_ok=True)
    note = render_note(memo)
    if not dry_run:
        path.write_text(note, encoding="utf-8")
        state.memo_paths[slug] = relative_state_path(path, vault_root)
    return path


def initial_cursor(days: int, full_history: bool) -> Tuple[int, str]:
    if full_history:
        return 0, ""
    start = dt.datetime.now().astimezone() - dt.timedelta(days=days)
    return int(start.timestamp()), ""


def run_sync(
    config_path: Path,
    vault_root: Path,
    state_path: Path,
    first_sync_days: int,
    full_history: bool,
    dry_run: bool,
) -> Dict[str, object]:
    config = load_flomo_config(config_path)
    inbox_dir = vault_root / "00_收件箱"
    state = SyncState.load(state_path)

    if state.cursor_updated_at:
        latest_updated_at = to_unix_timestamp(state.cursor_updated_at)
        latest_slug = state.cursor_slug
    else:
        latest_updated_at, latest_slug = initial_cursor(first_sync_days, full_history)

    fetched = 0
    written = 0
    skipped_deleted = 0
    updated_paths: List[str] = []

    while True:
        batch = fetch_updated_memos(config, latest_updated_at, latest_slug)
        if not batch:
            break

        fetched += len(batch)
        for memo in batch:
            result = sync_single_memo(memo, inbox_dir, vault_root, state, dry_run=dry_run)
            if result is None:
                skipped_deleted += 1
            else:
                written += 1
                updated_paths.append(str(result))

            latest_updated_at = to_unix_timestamp(str(memo.get("updated_at") or "1970-01-01 00:00:00"))
            latest_slug = str(memo.get("slug") or "")
            state.cursor_updated_at = str(memo.get("updated_at") or "")
            state.cursor_slug = latest_slug
            state.last_synced_at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
            if not dry_run:
                state.save()

        if len(batch) < 200:
            break

    return {
        "fetched": fetched,
        "written": written,
        "skipped_deleted": skipped_deleted,
        "updated_paths": updated_paths,
        "cursor_updated_at": state.cursor_updated_at,
        "cursor_slug": state.cursor_slug,
    }


def parse_args(argv: List[str]) -> argparse.Namespace:
    default_vault_root = Path(os.environ.get("CKW_VAULT_ROOT", Path.cwd() / "examples" / "demo-vault"))
    parser = argparse.ArgumentParser(description="Sync flomo memos into a Codex Knowledge Workflow Kit inbox.")
    parser.add_argument("--config-path", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--vault-root", type=Path, default=default_vault_root)
    parser.add_argument(
        "--state-path",
        type=Path,
        default=default_vault_root / ".state" / "flomo-sync" / "state.json",
    )
    parser.add_argument("--first-sync-days", type=int, default=30)
    parser.add_argument("--full-history", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    result = run_sync(
        config_path=args.config_path,
        vault_root=args.vault_root,
        state_path=args.state_path,
        first_sync_days=args.first_sync_days,
        full_history=args.full_history,
        dry_run=args.dry_run,
    )
    print(
        json.dumps(
            {
                "fetched": result["fetched"],
                "written": result["written"],
                "skipped_deleted": result["skipped_deleted"],
                "cursor_updated_at": result["cursor_updated_at"],
                "cursor_slug": result["cursor_slug"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
