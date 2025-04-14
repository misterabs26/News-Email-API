import streamlit as st
import smtplib, ssl
from email.mime.text import MIMEText


def send_email(topic, message):
    host = "smtp.gmail.com"
    port = 465

    admin_email = st.secrets["email"]["ADMIN_EMAIL"]
    admin_pw = st.secrets["email"]["ADMIN_PASS"]

    # News Data
    body = f"Here are the latest {topic} news articles:\n\n"
    for news in message:
        try:
            if news:
                news_title = news["title"] or "No Title"
                news_desc = news["description"] or "No Description"
                news_content = news["content"] or "No content"
                news_url = news["url"]
                body += (news_title + "\n" +
                         news_desc + "\n" +
                         news_content + "\n" +
                         news_url + 2*"\n")
            else:
                print("No articles found")
        except Exception as e:
            print(e)


    # Email format
    subject = f"{topic} News Digest"
    msg = MIMEText(body)
    msg["From"] = admin_email
    msg["To"] = admin_email
    msg["Subject"] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(admin_email,admin_pw)
        server.sendmail(admin_email,admin_email,msg.as_string())

