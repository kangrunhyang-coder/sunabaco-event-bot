import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

url = "https://sunabaco.com/event/"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

events = soup.select("a[href*='/event/']")

event_list = []
seen_links = set()

for event in events:

    link = event["href"]

    if not link.startswith("http"):
        link = "https://sunabaco.com" + link

    # 重複チェック
    if link in seen_links:
        continue

    seen_links.add(link)

    title = event.get_text(strip=True)

    if "開催" not in title:
        continue

    img = event.find("img")
    image_url = ""

    if img:
        image_url = img.get("src", "")

    event_list.append({
        "title": title,
        "link": link,
        "image": image_url
    })


if not event_list:
    print("イベントが見つかりませんでした")
    exit()


file_path = "last_event.txt"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_event = f.read()
else:
    last_event = ""


new_events = []

for event in event_list:

    if event["title"] != last_event:
        new_events.append(event)
    else:
        break


if not new_events:

    print("新しいイベントはありません")

else:

    print("新しいイベントがあります！")

    sender = "Kang.runhyang@gmail.com"
    password = "ymcm srgd cehm fexf"
    receiver = "Kang.runhyang@gmail.com"

    body = "<h2>SUNABACO 新イベント</h2>"

    for event in new_events:

        body += f"""
        <hr>
        <img src="{event['image']}" width="500">

        <p>{event['title']}</p>

        <a href="{event['link']}">
        イベントページを見る
        </a>
        """

    msg = MIMEText(body, "html")
    msg["Subject"] = "SUNABACO 新イベント通知"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

    with open(file_path, "w") as f:
        f.write(event_list[0]["title"])