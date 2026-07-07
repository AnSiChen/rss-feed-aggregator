from rss_feed_aggregator import load_articles


articles = load_articles()

for article in articles[:10]:

    print(article.source)
    print(article.title)
    print(article.author)
    print(article.published)
    print(article.link)
    print("-" * 60)
