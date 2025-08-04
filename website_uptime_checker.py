#sends mail for every 60 sec (we can change the time interval too)and sends only if the site is down
# import requests
# import time
# from datetime import datetime
# import smtplib
# from email.message import EmailMessage



# websites = [
#     "https://www.google.com",
#     "https://www.github.com",
#     "https://nonexistent1234xyz.com"
# ]

# check_interval = 60  # seconds between checks

# # Email setup (Gmail)
# EMAIL_ADDRESS = "vijayarayalupenumuri@gmail.com"
# EMAIL_PASSWORD = "fyee hccy zxgt oykp"  # Use app password if 2FA is enabled
# RECEIVER_EMAIL = "vijayarayalu64@gmail.com"


# def check_website(url):
#     try:
#         response = requests.get(url, timeout=10)
#         return response.status_code == 200
#     except requests.RequestException:
#         return False

# def log_status(url, status):
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     status_msg = f"[{now}] {url} is {'UP ✅' if status else 'DOWN ❌'}"
#     print(status_msg)
#     with open("uptime_log.txt", "a", encoding="utf-8") as f:

#         f.write(status_msg + "\n")

# def send_email_alert(url):
#     msg = EmailMessage()
#     msg.set_content(f"🚨 ALERT: The website {url} is DOWN!")
#     msg['Subject'] = f"Website Down Alert: {url}"
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = RECEIVER_EMAIL

#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             smtp.send_message(msg)
#         print("📧 Email alert sent!")
#     except Exception as e:
#         print(f"❌ Email sending failed: {e}")



# print("🔍 Starting Website Uptime Monitor...\n")
# while True:
#     for url in websites:
#         status = check_website(url)
#         log_status(url, status)
#         if not status:
#             send_email_alert(url)
#     time.sleep(check_interval)

#sends mail only once that to when the website gets down,u get again mail when the website goes up and then gets down
import requests
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage


websites = [
    "https://www.google.com",
    "https://www.github.com",
    "https://nonexistent1234xyz.com"
]

check_interval = 60  # seconds between checks

# Email setup (Gmail)
EMAIL_ADDRESS = "vijayarayalupenumuri@gmail.com"
EMAIL_PASSWORD = "fyee hccy zxgt oykp"  # Use app password if 2FA is enabled
RECEIVER_EMAIL = "vijayarayalu64@gmail.com"

# Keep track of the last known status for each website
last_status = {url: True for url in websites}  # Assume all are UP initially



def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def log_status(url, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_msg = f"[{now}] {url} is {'UP ✅' if status else 'DOWN ❌'}"
    print(status_msg)
    with open("uptime_log.txt", "a", encoding="utf-8") as f:
        f.write(status_msg + "\n")

def send_email_alert(url):
    msg = EmailMessage()
    msg.set_content(f"🚨 ALERT: The website {url} is DOWN!")
    msg['Subject'] = f"Website Down Alert: {url}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email alert sent!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")



print("🔍 Starting Website Uptime Monitor...\n")

while True:
    for url in websites:
        status = check_website(url)
        log_status(url, status)

        # Only send an email if the site just went DOWN
        if not status and last_status[url]:  # Was UP before, now DOWN
            send_email_alert(url)

        # Update the last status
        last_status[url] = status

    time.sleep(check_interval)
#this shows the details of monotoring process(time ,date,up or down) saved in the log files
# def read_logs():
#     try:
#         with open("uptime_log.txt", "r", encoding="utf-8") as f:
#             logs = f.readlines()
#         return logs
#     except FileNotFoundError:
#         return []
# all_logs = read_logs()
# for entry in all_logs:
#     print(entry.strip())

