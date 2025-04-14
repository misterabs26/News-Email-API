
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

    # Email format
    subject = f"{topic} News Digest"
    msg = MIMEMultipart()
    msg["From"] = admin_email
    msg["To"] = admin_email
    msg["Subject"] = subject

    # News Data
    body = f"Here are the latest {topic} news articles:\n\n"
    for i, news in enumerate(message):
        try:
            if news:
                news_title = news["title"] or "No Title"
                news_desc = news["description"] or "No Description"
                news_content = news["content"] or "No content"
                image_url = news["image_url"] or None
                news_url = news["url"]

                body += (news_title + "\n" +
                         news_desc + "\n" +
                         news_content + "\n" +
                         news_url + 2 * "\n")

                if image_url:
                    try:
                        image_data = requests.get(image_url).content

                        # the image was converted into MIMEImage
                        img = MIMEImage(image_data)
                        img.add_header('Content-ID', f'<image{i}>')
                        img.add_header("Content-Disposition", "inline", filename=f"image{i}.jpg")
                        msg.attach(img)
                    except Exception as img_error:
                        body += "[Image failed to load]" + "\n"
                        print(f"Image {i} failed: {img_error}")

            else:
                print("No articles found")
        except Exception as e:
            print(f"Article {i} error: {e}")


    msg.attach(MIMEText(body,"plain"))

    # Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(admin_email,admin_pw)
        server.sendmail(admin_email,admin_email,msg.as_string())

