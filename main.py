import requests
import streamlit as st
import send_email as fn

api_key = "60d55ee3ea5442889806dcc059beb25b"
url = ("https://newsapi.org/v2/everything?q=tesla&"
       "from=2025-03-10&sortBy=publishedAt&apiKey="
       "60d55ee3ea5442889806dcc059beb25b")

# Make request
request = requests.get(url)

# Get a dictionary with data
content = request.json()

# Access the article titles and description
for article in content["articles"]:
    print(article["title"])
    print(article["description"])