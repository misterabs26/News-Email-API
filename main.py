import requests
import streamlit as st
import send_email as fn
from datetime import date
from dateutil.relativedelta import relativedelta

# Web Layout
st.header("Get the latest news today!")
news_topic = st.text_input("", placeholder="Search news about ..", key="topic")

if news_topic:
    # Get last week's date (if u want to get the last month's news)
    last_week = date.today() - relativedelta(days=7)
    formatted_date = last_week.strftime("%Y-%m-%d")

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
    for i, article in enumerate(content["articles"]):

        # For email newsletter
        body.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "content": article["content"],
            "image_url": article["urlToImage"]
        })

        # Displaying news on the webpage
        with st.container():
            st.subheader(article["title"])
            st.text(article["description"])
            if article["urlToImage"]:
                st.image(article["urlToImage"], use_container_width=True)
                with st.expander("Read more"):
                    st.text(article["content"])
                    st.success(article["url"])

    # fn.send_email(news_topic,body)

else:
    st.info("Please type anything in the search bar")