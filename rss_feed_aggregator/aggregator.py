from collections.abc import Iterable

from .feeds import FEEDS
from .models import Article, FeedSource
from .parser import load_feed


def load_articles(
    feeds: Iterable[FeedSource] | None = None,
    *,
    per_feed_limit: int | None = 4,
) -> list[Article]:
    """Load, combine, and newest-first sort articles from configured feeds.

    Args:
        feeds: Optional iterable of ``FeedSource`` objects. Defaults to ``FEEDS``.
        per_feed_limit: Maximum entries loaded from each feed. Use ``None`` to
            load every entry returned by each source.
    """

    if per_feed_limit is not None and per_feed_limit < 0:
        raise ValueError("per_feed_limit must be zero or greater")

    articles: list[Article] = []

    for source in FEEDS if feeds is None else feeds:
        articles.extend(load_feed(source, limit=per_feed_limit))

    articles.sort(key=lambda article: article.published, reverse=True)
    return articles
