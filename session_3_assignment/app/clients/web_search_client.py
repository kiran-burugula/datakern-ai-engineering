import feedparser

def get_stock_news(ticker):
    url = f"https://news.google.com/rss/search?q={ticker}"
    
    feed = feedparser.parse(url)

    if not feed.entries:
        return []

    news_list = []

    for entry in feed.entries[:3]:
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "source": entry.source.title
        })

    return news_list

if __name__ == "__main__":
    print(get_stock_news("TSLA"))