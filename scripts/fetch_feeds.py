#!/usr/bin/env python3
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedparser

ROOT = Path(__file__).resolve().parents[1]
FEEDS_FILE = ROOT / "docs" / "sources" / "news_feeds.md"
OUT_FILE = ROOT / "data" / "news_links.json"

MAX_PER_FEED = 8
MAX_TOTAL = 40
DAYS_BACK = 3


def parse_feed_list(md_path: Path) -> list[str]:
    urls: list[str] = []

    if not md_path.exists():
        raise FileNotFoundError(f"Feed list not found: {md_path}")

    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^https?://", line):
            urls.append(line)

    return urls


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def entry_datetime(entry: Any) -> datetime | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        value = getattr(entry, key, None)
        if value:
            try:
                return datetime(*value[:6], tzinfo=timezone.utc)
            except Exception:
                continue
    return None


def entry_datetime_iso(entry: Any) -> str | None:
    dt = entry_datetime(entry)
    return dt.isoformat() if dt else None


def entry_summary(entry: Any) -> str:
    candidates = [
        getattr(entry, "summary", ""),
        getattr(entry, "description", ""),
    ]

    if hasattr(entry, "content") and entry.content:
        try:
            first_content = entry.content[0]
            if isinstance(first_content, dict):
                candidates.append(first_content.get("value", ""))
            else:
                candidates.append(getattr(first_content, "value", ""))
        except Exception:
            pass

    for candidate in candidates:
        cleaned = clean_text(candidate)
        if cleaned:
            return cleaned[:500]

    return ""


def build_item(entry: Any, feed_url: str, source_title: str, source_homepage: str) -> dict[str, Any] | None:
    title = clean_text(getattr(entry, "title", ""))
    link = getattr(entry, "link", "").strip()

    if not title or not link:
        return None

    dt = entry_datetime(entry)
    dt_iso = dt.isoformat() if dt else None

    return {
        "title": title,
        "link": link,
        "source": source_title,
        "source_feed": feed_url,
        "source_homepage": source_homepage,
        "published_at": dt_iso,
        "summary": entry_summary(entry),
    }


def main() -> None:
    urls = parse_feed_list(FEEDS_FILE)
    items: list[dict[str, Any]] = []

    cutoff_ts = datetime.now(timezone.utc).timestamp() - DAYS_BACK * 24 * 3600
    processed_feeds = 0

    for url in urls:
        feed = feedparser.parse(url)
        processed_feeds += 1

        source_title = clean_text(getattr(feed.feed, "title", "")) or url
        source_homepage = getattr(feed.feed, "link", "").strip() or url

        for entry in feed.entries[:MAX_PER_FEED]:
            item = build_item(entry, url, source_title, source_homepage)
            if not item:
                continue

            if item["published_at"]:
                try:
                    ts = datetime.fromisoformat(item["published_at"]).timestamp()
                    if ts < cutoff_ts:
                        continue
                except Exception:
                    pass

            items.append(item)

    # De-dup by link
    seen_links: set[str] = set()
    deduped: list[dict[str, Any]] = []

    for item in items:
        if item["link"] in seen_links:
            continue
        seen_links.add(item["link"])
        deduped.append(item)

    # Sort newest first if published_at exists
    deduped.sort(
        key=lambda x: x["published_at"] or "",
        reverse=True,
    )

    deduped = deduped[:MAX_TOTAL]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "feeds_count": processed_feeds,
                "items_count": len(deduped),
                "items": deduped,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Processed {processed_feeds} feeds")
    print(f"Wrote {len(deduped)} items to {OUT_FILE}")


if __name__ == "__main__":
    main()
