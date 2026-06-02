#!/usr/bin/env python3
"""Fetch AI HOT public RSS feeds into the newsletter archive."""

from __future__ import annotations

import argparse
import html
import os
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo


VAULT_ROOT = Path(os.environ.get("CKW_VAULT_ROOT", Path.cwd() / "examples" / "demo-vault"))
NEWSLETTERS_ROOT = VAULT_ROOT / "50_Resources" / "Newsletters"
TZ = ZoneInfo("Asia/Shanghai")

FEEDS = {
    "AI-HOT-Selected": "https://aihot.virxact.com/feed.xml",
    "AI-HOT-Daily": "https://aihot.virxact.com/feed/daily.xml",
}
ALL_FEED = {"AI-HOT-All": "https://aihot.virxact.com/feed/all.xml"}


@dataclass
class RssItem:
    title: str
    link: str
    description: str
    pub_date: str
    author: str
    guid: str


def fetch_url(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ai-workflow-newsletter-archiver/1.0 (+https://aihot.virxact.com/agent)",
            "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")


def text_of(node: ET.Element, tag: str) -> str:
    child = node.find(tag)
    if child is None or child.text is None:
        return ""
    return html.unescape(child.text.strip())


def parse_items(xml_text: str) -> list[RssItem]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []
    items: list[RssItem] = []
    for item in channel.findall("item"):
        items.append(
            RssItem(
                title=text_of(item, "title"),
                link=text_of(item, "link"),
                description=clean_description(text_of(item, "description")),
                pub_date=format_pub_date(text_of(item, "pubDate")),
                author=clean_author(text_of(item, "author")),
                guid=text_of(item, "guid"),
            )
        )
    return items


def clean_description(value: str) -> str:
    value = re.sub(r"\r\n?", "\n", value).strip()
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value


def clean_author(value: str) -> str:
    match = re.search(r"\((.+)\)", value)
    return match.group(1).strip() if match else value.strip()


def format_pub_date(value: str) -> str:
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).astimezone(TZ).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return value


def month_dir_for(date_text: str) -> Path:
    return NEWSLETTERS_ROOT / date_text[:7]


def write_raw_file(raw_dir: Path, date_text: str, source: str, xml_text: str) -> Path:
    path = raw_dir / f"{date_text}_{source}-Raw.xml"
    path.write_text(xml_text, encoding="utf-8")
    return path


def render_markdown(
    date_text: str,
    fetched_at: str,
    source_items: dict[str, list[RssItem]],
    warnings: dict[str, str],
) -> str:
    lines = [
        "---",
        "type: newsletter-raw-digest",
        "source: AI HOT",
        f"created: {date_text}",
        "status: captured",
        "tags:",
        "  - newsletters",
        "  - ai",
        "  - aihot",
        "---",
        f"# {date_text} AI HOT Fetch Summary",
        "",
        f"- Fetched at: {fetched_at}",
        "- Access method: public RSS",
        "- Site: https://aihot.virxact.com/agent",
        "",
    ]

    if warnings:
        lines.extend(["## Fetch Warnings", ""])
        for source, warning in warnings.items():
            lines.append(f"- {source}: {warning}")
        lines.append("")

    for source, items in source_items.items():
        lines.extend([f"## {source}", "", f"- Item count: {len(items)}", ""])
        for idx, item in enumerate(items[:30], start=1):
            lines.append(f"### {idx}. {item.title or item.guid or 'Untitled item'}")
            if item.pub_date:
                lines.append(f"- Time: {item.pub_date}")
            if item.author:
                lines.append(f"- Source: {item.author}")
            if item.link:
                lines.append(f"- Link: {item.link}")
            if item.description:
                lines.extend(["", item.description])
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch AI HOT RSS feeds into 50_Resources/Newsletters.")
    parser.add_argument("--date", default=datetime.now(TZ).strftime("%Y-%m-%d"), help="archive date, default today")
    parser.add_argument("--include-all", action="store_true", help="also fetch the full AI HOT feed")
    parser.add_argument("--delay", type=float, default=10.0, help="seconds between feed requests")
    args = parser.parse_args()

    feeds = dict(FEEDS)
    if args.include_all:
        feeds.update(ALL_FEED)

    month_dir = month_dir_for(args.date)
    raw_dir = month_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    fetched_at = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")
    source_items: dict[str, list[RssItem]] = {}
    raw_paths: list[Path] = []
    warnings: dict[str, str] = {}

    for index, (source, url) in enumerate(feeds.items()):
        if index:
            time.sleep(args.delay)
        try:
            xml_text = fetch_url(url)
        except urllib.error.HTTPError as exc:
            if exc.code == 304:
                warnings[source] = "Source returned HTTP 304 Not Modified without XML content"
                print(f"warning={source}: HTTP 304 Not Modified")
                continue
            warnings[source] = f"HTTP {exc.code}: {exc.reason}"
            print(f"warning={source}: HTTP {exc.code} {exc.reason}")
            continue
        except urllib.error.URLError as exc:
            warnings[source] = f"URL error: {exc.reason}"
            print(f"warning={source}: URL error {exc.reason}")
            continue
        raw_paths.append(write_raw_file(raw_dir, args.date, source, xml_text))
        source_items[source] = parse_items(xml_text)

    if not source_items:
        for source, warning in warnings.items():
            print(f"{source}=0 ({warning})")
        return 1

    summary_path = month_dir / f"{args.date}_AI-HOT-summary.md"
    summary_path.write_text(render_markdown(args.date, fetched_at, source_items, warnings), encoding="utf-8")

    print(f"summary={summary_path}")
    for path in raw_paths:
        print(f"raw={path}")
    for source, items in source_items.items():
        print(f"{source}={len(items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
