import os
import feedparser
import requests
from datetime import datetime
from dateutil import parser as date_parser

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_COUNT = int(os.getenv("NEWS_COUNT", 5))
RSS_FEEDS = os.getenv("RSS_FEEDS", "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml").split(",")

def fetch_news():
    all_articles = []
    for feed_url in RSS_FEEDS:
        one_site_articles = []
        feed = feedparser.parse(feed_url.strip())
        # for entry in feed.entries:
        #     pub_date = None
        #     if hasattr(entry, "published"):
        #         try:
        #             pub_date = date_parser.parse(entry.published)
        #         except Exception:
        #             pub_date = None
        #     one_site_articles.append({
        #         "title": entry.title,
        #         "link": entry.link,
        #         "published": pub_date
        #     })
        all_articles += feed.entries[:NEWS_COUNT]
    # 日付があるものは新しい順に、なければ後回し
    # all_articles.sort(key=lambda x: x["published"] or datetime.min, reverse=True)
    return all_articles

def send_to_discord(articles):
    embeds = []
    for a in articles:
        embed = {
            "title": a.title,          # 記事タイトル
            "url": a.link,             # クリックで飛べるリンク
            "description": (a.summary if hasattr(a, "summary") else "（要約なし）"),
            "color": 0x1E90FF          # 青色（16進数カラーコード）
        }
        embeds.append(embed)

    data = {
        "content": "📰 今日のITニュースはこちら！",
        "embeds": embeds
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Discordに送信しました！（Embed形式）")
    else:
        print(f"⚠️ Discord送信失敗: {response.status_code}, {response.text}")

if __name__ == "__main__":
    news = fetch_news()
    send_to_discord(news)
