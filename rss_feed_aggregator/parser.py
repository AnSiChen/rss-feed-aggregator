from datetime import datetime

import feedparser
from bs4 import BeautifulSoup

from .models import Article


def extract_image(entry) -> str | None:
    """Extract first image from an RSS entry"""

    if not hasattr(entry, "content"):
        return None

    soup = BeautifulSoup(
        entry.content[0].value,
        "html.parser"
    )

    image = soup.find("img")

    if image:
        return image.get("src")

    return None


def load_feed(name: str, url: str) -> list[Article]:
    """Download and normalize single RSS feed."""

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:

        articles.append(
            Article(
                title=entry.title,
                summary=entry.summary,
                author=getattr(entry, "author", name),
                published=datetime(*entry.published_parsed[:6]),
                link=entry.link,
                image=extract_image(entry),
                source=name,
            )
        )

    return articles
