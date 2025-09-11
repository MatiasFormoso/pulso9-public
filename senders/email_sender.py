import os, smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER or "")

def send_email(to_email: str, subject: str, body: str):
    if not (EMAIL_USER and EMAIL_PASS and EMAIL_FROM):
        print("[email_sender] Missing EMAIL_USER/EMAIL_PASS/EMAIL_FROM. Preview mode.")
        print("To:", to_email)
        print("Subject:", subject)
        print(body)
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = EMAIL_FROM if "<" in EMAIL_FROM else formataddr(("Pulso 9", EMAIL_USER))
    msg["To"] = to_email
    msg["Subject"] = subject

    ctx = ssl.create_default_context()
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls(context=ctx)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [to_email], msg.as_string())
        print("[email_sender] Email sent")
