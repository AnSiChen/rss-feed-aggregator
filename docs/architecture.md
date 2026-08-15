# Architecture

RSS Feed Aggregator is intentionally framework-independent. It performs one job: convert multiple external RSS/Atom feeds into one normalized, newest-first collection of Python objects.

```text
Configured FeedSource objects
            │
            ▼
       feedparser
            │
            ▼
        parser.py
   ┌────────┼─────────┐
   │        │         │
 dates   summaries   images
   └────────┼─────────┘
            ▼
         Article
            │
            ▼
      aggregator.py
            │
            ▼
  newest-first article list
```

## Components

### `models.py`

Defines the normalized `Article` model and the `FeedSource` configuration model. Presentation layers can use `Article.source_label` when they want a combined category/publication label.

### `feeds.py`

Contains the default curated source configuration. The aggregator is not coupled to those feeds; callers may supply their own `FeedSource` iterable to `load_articles()`.

### `parser.py`

Downloads one feed and normalizes its entries. It handles:

- `published_parsed` with `updated_parsed` fallback;
- HTML removal and whitespace normalization in summaries;
- configurable summary truncation;
- Media RSS `media:content` images;
- Media RSS thumbnails;
- images embedded in content HTML;
- images embedded in summaries;
- image enclosures;
- missing titles, authors, summaries, links, dates, and images.

### `aggregator.py`

Loads each configured source, combines normalized articles, and sorts the result by publication time. The per-feed entry limit is configurable.

## Deliberately excluded

The original portfolio integration also handled internal Markdown articles, featured-content selection, request-time caching, Jinja templates, and Flask routes. That belongs to the consuming app (my portfolio), not the aggregation engine.
