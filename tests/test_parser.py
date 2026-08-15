from datetime import datetime
import unittest
from unittest.mock import patch

from rss_feed_aggregator.models import FeedSource
from rss_feed_aggregator.parser import (
    clean_summary,
    extract_image,
    load_feed,
    parse_date,
)


class ParserTests(unittest.TestCase):
    def test_parse_date_prefers_published(self):
        entry = {
            "published_parsed": (2026, 8, 15, 10, 30, 0, 0, 0, 0),
            "updated_parsed": (2026, 8, 16, 10, 30, 0, 0, 0, 0),
        }

        self.assertEqual(parse_date(entry), datetime(2026, 8, 15, 10, 30))

    def test_parse_date_falls_back_to_updated(self):
        entry = {
            "updated_parsed": (2026, 8, 14, 8, 0, 0, 0, 0, 0),
        }

        self.assertEqual(parse_date(entry), datetime(2026, 8, 14, 8, 0))

    def test_parse_date_uses_datetime_min_when_date_missing(self):
        self.assertEqual(parse_date({}), datetime.min)

    def test_clean_summary_strips_html_and_collapses_whitespace(self):
        summary = "<p>Hello   <strong>world</strong>.</p>\n<p>More text.</p>"
        self.assertEqual(clean_summary(summary), "Hello world . More text.")

    def test_clean_summary_truncates_at_word_boundary(self):
        summary = "one two three four five"
        self.assertEqual(clean_summary(summary, max_length=13), "one two...")

    def test_extract_image_prefers_media_content(self):
        entry = {
            "media_content": [{"url": "https://example.test/media.jpg"}],
            "media_thumbnail": [{"url": "https://example.test/thumb.jpg"}],
            "summary": '<img src="https://example.test/summary.jpg">',
        }

        self.assertEqual(
            extract_image(entry),
            "https://example.test/media.jpg",
        )

    def test_extract_image_uses_html_summary(self):
        entry = {
            "summary": '<p>Story</p><img src="https://example.test/summary.jpg">',
        }

        self.assertEqual(
            extract_image(entry),
            "https://example.test/summary.jpg",
        )

    def test_extract_image_uses_image_enclosure(self):
        entry = {
            "links": [
                {
                    "rel": "enclosure",
                    "type": "image/jpeg",
                    "href": "https://example.test/enclosure.jpg",
                }
            ]
        }

        self.assertEqual(
            extract_image(entry),
            "https://example.test/enclosure.jpg",
        )

    @patch("rss_feed_aggregator.parser.feedparser.parse")
    def test_load_feed_normalizes_entry(self, parse_mock):
        parse_mock.return_value.entries = [
            {
                "title": "A story",
                "summary": "<p>A useful summary.</p>",
                "published_parsed": (2026, 8, 15, 9, 0, 0, 0, 0, 0),
                "link": "https://example.test/story",
            }
        ]

        source = FeedSource(
            name="Example",
            url="https://example.test/feed.xml",
            category="Science",
            default_author="Example Publication",
        )

        articles = load_feed(source, limit=1)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "A story")
        self.assertEqual(articles[0].summary, "A useful summary.")
        self.assertEqual(articles[0].author, "Example Publication")
        self.assertEqual(articles[0].source, "Example")
        self.assertEqual(articles[0].category, "Science")
        self.assertEqual(articles[0].source_label, "Science • Example")


if __name__ == "__main__":
    unittest.main()
