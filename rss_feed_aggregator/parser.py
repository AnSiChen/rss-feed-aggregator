from __future__ import annotations

from datetime import datetime
import re
from typing import Any

import feedparser
from bs4 import BeautifulSoup

from .models import Article, FeedSource


def parse_date(entry: Any) -> datetime:
    """Return the best publication timestamp available on an RSS entry.

    ``published_parsed`` is preferred, followed by ``updated_parsed``. Entries
    without either value receive ``datetime.min`` so an undated item does not
    incorrectly appear newer than dated articles when the aggregate is sorted.
    """

    for field in ("published_parsed", "updated_parsed"):
        parsed = _entry_get(entry, field)
        if parsed:
            try:
                return datetime(*parsed[:6])
            except (TypeError, ValueError):
                continue

    return datetime.min


def clean_summary(summary: str | None, max_length: int = 180) -> str:
    """Strip HTML/duplicate whitespace and truncate an RSS summary."""

    if not summary:
        return ""

    text = BeautifulSoup(str(summary), "html.parser").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_length:
        return text

    shortened = text[:max_length].rsplit(" ", 1)[0].rstrip()
    if not shortened:
        shortened = text[:max_length].rstrip()

    return f"{shortened}..."


def extract_image(entry: Any) -> str | None:
    """Extract an article image using common RSS/Atom conventions.

    Extraction order mirrors the mature implementation used by the original
    portfolio integration: Media RSS content, Media RSS thumbnail, HTML
    content, HTML summary, and finally image enclosures.
    """

    media_content = _entry_get(entry, "media_content") or []
    if media_content:
        url = _mapping_get(media_content[0], "url")
        if url:
            return url

    media_thumbnail = _entry_get(entry, "media_thumbnail") or []
    if media_thumbnail:
        url = _mapping_get(media_thumbnail[0], "url")
        if url:
            return url

    content = _entry_get(entry, "content") or []
    if content:
        value = _mapping_get(content[0], "value")
        image = _first_html_image(value)
        if image:
            return image

    summary = _entry_get(entry, "summary")
    image = _first_html_image(summary)
    if image:
        return image

    links = _entry_get(entry, "links") or []
    for link in links:
        rel = _mapping_get(link, "rel")
        media_type = _mapping_get(link, "type") or ""
        href = _mapping_get(link, "href")

        if rel == "enclosure" and str(media_type).startswith("image/") and href:
            return href

    return None


def load_feed(source: FeedSource, limit: int | None = None) -> list[Article]:
    """Download one RSS feed and normalize its entries into ``Article`` objects."""

    feed = feedparser.parse(source.url)
    entries = list(getattr(feed, "entries", []) or [])

    if limit is not None:
        if limit < 0:
            raise ValueError("limit must be zero or greater")
        entries = entries[:limit]

    articles: list[Article] = []

    for entry in entries:
        title = str(_entry_get(entry, "title") or "Untitled").strip()
        summary = clean_summary(
            _entry_get(entry, "summary") or _entry_get(entry, "description") or ""
        )
        author = str(
            _entry_get(entry, "author")
            or source.default_author
            or source.name
        ).strip()
        link = str(_entry_get(entry, "link") or "").strip()

        articles.append(
            Article(
                title=title,
                summary=summary,
                author=author,
                published=parse_date(entry),
                link=link,
                image=extract_image(entry),
                source=source.name,
                category=source.category,
            )
        )

    return articles


def _entry_get(entry: Any, key: str, default: Any = None) -> Any:
    if hasattr(entry, "get"):
        try:
            return entry.get(key, default)
        except TypeError:
            pass

    return getattr(entry, key, default)


def _mapping_get(value: Any, key: str, default: Any = None) -> Any:
    if hasattr(value, "get"):
        return value.get(key, default)
    return getattr(value, key, default)


def _first_html_image(html: str | None) -> str | None:
    if not html:
        return None

    soup = BeautifulSoup(str(html), "html.parser")
    image = soup.find("img")

    if image:
        src = image.get("src")
        if src:
            return str(src)

    return None
