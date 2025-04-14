import streamlit as st
import smtplib, ssl
from email.mime.text import MIMEText


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    admin_email = st.secrets["email"]["ADMIN_EMAIL"]
    admin_pw = st.secrets["email"]["ADMIN_PASS"]

    # News Data
    body = "Here are the latest Tesla news articles:\n\n"
    for news in message:
        news_title = news["title"]
        news_desc = news["description"]
        body += news_title +"\n" + news_desc + 2*"\n"

    # Email format
    subject = "Tesla News Digest"
    msg = MIMEText(body)
    msg["From"] = admin_email
    msg["To"] = admin_email
    msg["Subject"] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(admin_email,admin_pw)
        server.sendmail(admin_email,admin_email,msg.as_string())

