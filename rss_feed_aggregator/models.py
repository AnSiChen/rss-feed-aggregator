from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class FeedSource:
    """Configuration for a single RSS source."""

    name: str
    url: str
    category: str
    default_author: str | None = None

    @property
    def label(self) -> str:
        """Human-readable source label suitable for presentation layers."""

        return f"{self.category} • {self.name}"


@dataclass(slots=True)
class Article:
    """Normalized article produced from an RSS entry."""

    title: str
    summary: str
    author: str
    published: datetime
    link: str
    image: str | None
    source: str
    category: str

    @property
    def source_label(self) -> str:
        """Return a display label combining category and publication."""

        return f"{self.category} • {self.source}"
