import requests
import streamlit as st
import send_email as fn
from datetime import date
from dateutil.relativedelta import relativedelta

# Get last week's date (if u want to get the last month's news)
last_week = date.today() - relativedelta(days=7)
formatted_date = last_week.strftime("%Y-%m-%d")

news_topic = "Philippines"
api_key = "60d55ee3ea5442889806dcc059beb25b"
url = (f"https://newsapi.org/v2/everything?"
       f"q={news_topic}&"
       f"from={last_week}&"
       f"sortBy=relevancy&"
       f"apiKey=60d55ee3ea5442889806dcc059beb25b&"
       f"language=en&"
       f"pageSize=15")

# Make request
request = requests.get(url)

# Get a dictionary with data
content = request.json()

# Access the article titles and description
body = []
for article in content["articles"]:
    body.append({
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "content": article["content"]
    })
fn.send_email(news_topic,body)