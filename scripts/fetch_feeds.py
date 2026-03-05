import feedparser
import json

feeds = [
    "https://openai.com/blog/rss",
    "https://arxiv.org/rss/cs.AI",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
]

items = []

for url in feeds:
    feed = feedparser.parse(url)

    for entry in feed.entries[:5]:
        items.append({
            "title": entry.title,
            "link": entry.link
        })

with open("news_links.json", "w") as f:
    json.dump(items, f)
