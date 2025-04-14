import requests
import streamlit as st
import send_email as fn
from datetime import date
from dateutil.relativedelta import relativedelta

# Get last month's date
last_month = date.today() - relativedelta(months=1)
formatted_date = last_month.strftime("%Y-%m-%d")

api_key = "60d55ee3ea5442889806dcc059beb25b"
url = (f"https://newsapi.org/v2/everything?q=tesla&from={formatted_date}"
       f"&sortBy=publishedAt&apiKey=60d55ee3ea5442889806dcc059beb25b")

# Make request
request = requests.get(url)

# Get a dictionary with data
content = request.json()

# Access the article titles and description
body = []
for article in content["articles"]:
    body.append({
        "title": article["title"],
        "description": article["description"]
    })
fn.send_email(body)