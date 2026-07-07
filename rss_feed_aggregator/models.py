from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Article:
    """Represents a normalized article from an RSS feed."""

    title: str
    summary: str
    author: str
    published: datetime

    link: str
    image: str | None

    source: str
