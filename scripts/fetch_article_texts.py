#!/usr/bin/env python3
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / "data" / "news_links.json"
OUT_FILE = ROOT / "data" / "news_articles.json"

MAX_TEXT_LENGTH = 12000


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    article = soup.find("article")
    if article:
        text = article.get_text(" ", strip=True)
        return clean_text(text)[:MAX_TEXT_LENGTH]

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
    return clean_text(text)[:MAX_TEXT_LENGTH]


def main():
    payload = json.loads(IN_FILE.read_text(encoding="utf-8"))
    items = payload["items"] if isinstance(payload, dict) else payload

    enriched = []

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; AIContentBot/1.0; +https://github.com)"
        }
    )

    for item in items:
        article_text = ""
        try:
            response = session.get(item["link"], timeout=20)
            response.raise_for_status()
            article_text = extract_text_from_html(response.text)
        except Exception as e:
            article_text = f"FETCH_ERROR: {e}"

        enriched.append(
            {
                **item,
                "article_text": article_text,
            }
        )

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(
            {
                "items_count": len(enriched),
                "items": enriched,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {len(enriched)} enriched articles to {OUT_FILE}")


if __name__ == "__main__":
    main()
