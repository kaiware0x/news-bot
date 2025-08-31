import os
import feedparser
import requests
from datetime import datetime
from dateutil import parser as date_parser

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_COUNT = int(os.getenv("NEWS_COUNT", 5))
RSS_FEEDS = os.getenv("RSS_FEEDS", "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml").split(",")

def fetch_news():
    all_articles = {}
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url.strip())
        all_articles[feed_url] = feed.entries[:NEWS_COUNT]
    return all_articles

def send_to_discord(all_articles: dict):
    for feed_url, articles in all_articles.items():
        embeds  = []
        for a in articles:
            embed = {
                "title": a.title,          # 記事タイトル
                "url": a.link,             # クリックで飛べるリンク
                "description": (a.summary if hasattr(a, "summary") else "（要約なし）"),
                "color": 0x1E90FF          # 青色（16進数カラーコード）
            }
            embeds.append(embed)

        data = {
            "content": f"📰 今日のITニュース on {feed_url}",
            "embeds": embeds
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"✅ Discordに送信しました: {feed_url}")
        else:
            print(f"⚠️ Discord送信失敗: {response.status_code}, {response.text}")

if __name__ == "__main__":
    news = fetch_news()
    send_to_discord(news)
