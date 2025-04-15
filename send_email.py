
import streamlit as st
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests

def send_email(topic, message):
    host = "smtp.gmail.com"
    port = 465

    admin_email = st.secrets["email"]["ADMIN_EMAIL"]
    admin_pw = st.secrets["email"]["ADMIN_PASS"]

    receiver_email = "ayeras.gerald26@gmail.com"

    # Email format
    subject = f"{topic} News Digest"
    msg = MIMEMultipart()
    msg["From"] = admin_email
    msg["To"] = admin_email
    msg["Subject"] = subject

    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    # News Data
    html_body = f"<h1>{topic.title()} News Digest</h1><br>"
    for i, news in enumerate(message):
        try:
            news_title = news["title"] or "No Title"
            news_desc = news["description"] or "No Description"
            news_content = news["content"] or "No content"
            image_url = news["image_url"] or None
            news_url = news["url"]

            html_body += f"""
                <h2>{news_title}</h2>
                <p><strong>{news_desc}</strong></p>
            """

            if image_url:
                try:
                    image_data = requests.get(image_url)
                    response = image_data.content

                    # the image was converted into MIMEImage
                    img = MIMEImage(response)
                    img.add_header("Content-ID", f"<image{i}>")
                    img.add_header("Content-Disposition", "inline", filename=f"image{i}.jpg")
                    msg.attach(img)

                    html_body += f'<img src="cid:image{i}" width="500"/><br>'
                except Exception as e:
                    print(f"Image failed to load: {e}")
                    html_body += "[Image failed to load]<br>"

            html_body += f"""
                            <p>{news_content}</p>
                            <a href="{news_url}">Read more</a>
                            <hr>
                        """
        except Exception as e:
            print(f"Article {i} error: {e}")


    msg_alternative.attach(MIMEText(html_body, "html"))

    # Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(admin_email,admin_pw)
        server.sendmail(admin_email,receiver_email,msg.as_string())

