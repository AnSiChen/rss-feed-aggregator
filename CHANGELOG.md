# Changelog

## 2026-08-15

- Expanded the original NASA-only source configuration to the curated source set used by the mature portfolio integration.
- Replaced source-specific loader duplication with the reusable `FeedSource` + `load_feed()` pipeline.
- Added publication-date fallback handling.
- Added HTML/whitespace summary normalization and configurable truncation.
- Added Media RSS, embedded HTML, summary, and enclosure image extraction strategies.
- Added fallback handling for incomplete feed entries.
- Added category metadata and `source_label` to normalized articles.
- Added configurable per-feed aggregation limits.
- Added network-free parser and aggregator unit tests.
- Kept Flask, Jinja, internal Markdown articles, featured-selection logic, and application caching outside the package.
- Added runtime dependencies, `.gitignore`, documentation refresh, and MIT license text.
