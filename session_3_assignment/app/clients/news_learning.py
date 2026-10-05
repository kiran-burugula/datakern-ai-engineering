import feedparser

url = "https://news.google.com/rss/search?q=TSLA"

feed = feedparser.parse(url)

# print(len(feed.entries))
# print(feed.entries[0])

entry = feed.entries[0]

news_item = {
    "title": entry.title,
    "link": entry.link,
    "published": entry.published,
    "source": entry.source.title
}
print(news_item)

for entry in feed.entries[:3]:
    print("Title:",entry.title)