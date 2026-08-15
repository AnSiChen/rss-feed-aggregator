from datetime import datetime
import unittest
from unittest.mock import patch

from rss_feed_aggregator import Article, FeedSource
from rss_feed_aggregator.aggregator import load_articles


class AggregatorTests(unittest.TestCase):
    @patch("rss_feed_aggregator.aggregator.load_feed")
    def test_combines_and_sorts_articles_newest_first(self, load_feed_mock):
        first = FeedSource("First", "https://first.test/feed", "Science")
        second = FeedSource("Second", "https://second.test/feed", "Ideas")

        older = Article(
            title="Older",
            summary="",
            author="First",
            published=datetime(2026, 8, 10),
            link="https://first.test/older",
            image=None,
            source="First",
            category="Science",
        )
        newer = Article(
            title="Newer",
            summary="",
            author="Second",
            published=datetime(2026, 8, 15),
            link="https://second.test/newer",
            image=None,
            source="Second",
            category="Ideas",
        )

        load_feed_mock.side_effect = [[older], [newer]]

        articles = load_articles([first, second], per_feed_limit=3)

        self.assertEqual([article.title for article in articles], ["Newer", "Older"])
        self.assertEqual(load_feed_mock.call_count, 2)
        for call in load_feed_mock.call_args_list:
            self.assertEqual(call.kwargs["limit"], 3)

    def test_negative_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            load_articles([], per_feed_limit=-1)


if __name__ == "__main__":
    unittest.main()
