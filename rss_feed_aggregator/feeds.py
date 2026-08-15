from .models import FeedSource


FEEDS = [
    FeedSource(
        name="NASA",
        url="https://www.nasa.gov/rss/dyn/breaking_news.rss",
        category="Space",
        default_author="NASA",
    ),
    FeedSource(
        name="Ars Technica",
        url="https://feeds.arstechnica.com/arstechnica/index",
        category="Technology",
        default_author="Ars Technica",
    ),
    FeedSource(
        name="Quanta Magazine",
        url="https://www.quantamagazine.org/feed/",
        category="Science",
        default_author="Quanta Magazine",
    ),
    FeedSource(
        name="Nautilus",
        url="https://nautil.us/feed/",
        category="Science",
        default_author="Nautilus",
    ),
    FeedSource(
        name="MIT Technology Review",
        url="https://www.technologyreview.com/feed/",
        category="Technology",
        default_author="MIT Technology Review",
    ),
    FeedSource(
        name="Smithsonian Magazine",
        url="https://www.smithsonianmag.com/rss/latest_articles/",
        category="Exploration / History",
        default_author="Smithsonian Magazine",
    ),
    FeedSource(
        name="Aeon",
        url="https://aeon.co/feed.rss",
        category="Ideas",
        default_author="Aeon",
    ),
    FeedSource(
        name="Atlas Obscura",
        url="https://www.atlasobscura.com/feeds/latest",
        category="Exploration",
        default_author="Atlas Obscura",
    ),
]
