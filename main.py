import os
import time
import asyncio

import pandas as pd
import feedparser
import schedule

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

watchlist = pd.read_csv("watchlist.csv")


def get_news(keyword):

    url = f"https://news.google.com/rss/search?q={keyword}"

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries[:3]:

        news.append({
            "title": entry.title,
            "link": entry.link
        })

    return news


def summarize_news(text):

    return "AI 요약 테스트"

    # 나중에 OpenAI 연결 시 사용
    # response = client.chat.completions.create(
    #     model="gpt-4.1-mini",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "주식 투자 관점에서 핵심만 짧게 요약"
    #         },
    #         {
    #             "role": "user",
    #             "content": text
    #         }
    #     ]
    # )

    # return response.choices[0].message.content


def send_watchlist_news():

    for _, row in watchlist.iterrows():

        name = row["name"]

        news_list = get_news(name)

        if not news_list:
            continue

        first_news = news_list[0]

        summary = summarize_news(
            first_news["title"]
        )

        message = f"""
📌 {name}

📰 {first_news['title']}

🤖 AI 요약
{summary}

🔗 {first_news['link']}
"""

        asyncio.run(
            bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )
        )

        time.sleep(3)


schedule.every(1).hours.do(
    send_watchlist_news
)

send_watchlist_news()

while True:

    schedule.run_pending()

    time.sleep(10)