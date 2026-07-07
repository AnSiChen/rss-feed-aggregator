# Architecture

RSS Feed Aggregator has four small module.

```
RSS Feed
    │
    ▼
feedparser
    │
    ▼
Parser
    │
    ▼
Article
    │
    ▼
Aggregator
    │
    ▼
Sorted Article List
```

## Components

### feeds.py

RSS feed sources that will be aggregated.

### parser.py

Downloads RSS feeds, extracts article metadata, parses embedded images, and converts entries into normalized `Article` objects.

### models.py

`Article` data model used throughout the package.

### aggregator.py

Loads every feed, combines all articles into one collection, sorts them by publication date, and returns final list.
