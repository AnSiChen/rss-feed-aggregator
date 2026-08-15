from rss_feed_aggregator import load_articles


articles = load_articles(per_feed_limit=4)

for article in articles[:10]:
    print(article.source_label)
    print(article.title)
    print(article.author)
    print(article.published)
    print(article.link)
    print(article.image or "No feed image")
    print("-" * 60)
