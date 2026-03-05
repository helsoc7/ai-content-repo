#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parents[1]
FEEDS_FILE = ROOT / "docs" / "sources" / "news_feeds.md"
OUT_FILE = ROOT / "data" / "news_links.json"

MAX_PER_FEED = 8          # wie viele Items pro Feed
MAX_TOTAL = 40            # Gesamtlimit
DAYS_BACK = 3             # nur Einträge der letzten X Tage, wenn Datum vorhanden


def parse_feed_list(md_path: Path) -> list[str]:
    urls = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # simple URL check
        if re.match(r"^https?://", line):
            urls.append(line)
    return urls


def entry_date(entry) -> str | None:
    # feedparser gives *_parsed as time.struct_time
    for key in ("published_parsed", "updated_parsed"):
        if key in entry and entry[key]:
            dt = datetime(*entry[key][:6], tzinfo=timezone.utc)
            return dt.isoformat()
    return None


def main():
    urls = parse_feed_list(FEEDS_FILE)
    items = []

    cutoff = datetime.now(timezone.utc).timestamp() - DAYS_BACK * 24 * 3600

    for url in urls:
        feed = feedparser.parse(url)
        source_title = getattr(feed.feed, "title", None) or url

        for entry in feed.entries[:MAX_PER_FEED]:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            if not title or not link:
                continue

            dt_iso = entry_date(entry)
            # Filter by age if we have a timestamp
            if dt_iso:
                try:
                    ts = datetime.fromisoformat(dt_iso.replace("Z", "+00:00")).timestamp()
                    if ts < cutoff:
                        continue
                except Exception:
                    pass

            items.append(
                {
                    "title": title,
                    "link": link,
                    "source": source_title,
                    "published_at": dt_iso,
                }
            )

    # De-dup by link
    seen = set()
    deduped = []
    for it in items:
        if it["link"] in seen:
            continue
        seen.add(it["link"])
        deduped.append(it)

    deduped = deduped[:MAX_TOTAL]

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(deduped, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {len(deduped)} items to {OUT_FILE}")


if __name__ == "__main__":
    main()
