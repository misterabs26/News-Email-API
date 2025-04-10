import streamlit as st
import smtplib, ssl
from email.mime.text import MIMEText


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    admin_email = st.secrets["email"]["ADMIN_EMAIL"]
    admin_pw = st.secrets["email"]["ADMIN_PASS"]

    # Email format
    subject = "Daily News"
    body = f"""
    {message}
    """
    msg = MIMEText(body)
    msg["From"] = admin_email
    msg["To"] = admin_email
    msg["Subject"] = subject


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host,port,context =context) as server:
        server.login(admin_email,admin_pw)
        server.sendmail(admin_email,admin_email,msg.as_string())

