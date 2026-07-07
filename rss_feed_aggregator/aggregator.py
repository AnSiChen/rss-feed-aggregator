from .feeds import FEEDS
from .parser import load_feed


def load_articles():
    """Load and combine articles from all RSS feeds."""

    articles = []

    for feed in FEEDS:
        articles.extend(
            load_feed(
                feed["name"],
                feed["url"],
            )
        )

    articles.sort(
        key=lambda article: article.published,
        reverse=True,
    )

    return articles
