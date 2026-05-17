import smtplib
from email.message import EmailMessage
import requests
from typing import Dict, Any
from .logger import get_logger

log = get_logger(__name__)

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.base_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def send(self, text: str):
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            resp = requests.post(self.base_url, json=payload, timeout=5)
            resp.raise_for_status()
            log.info("Telegram notification sent")
        except Exception as exc:
            log.error("Failed to send Telegram alert: %s", exc)

class EmailNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, from_addr: str, to_addrs: list):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.to_addrs = to_addrs

    def send(self, subject: str, body: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.to_addrs)
        msg.set_content(body)
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
                s.starttls()
                s.login(self.username, self.password)
                s.send_message(msg)
            log.info("Email notification sent")
        except Exception as exc:
            log.error("Failed to send email alert: %s", exc)

def build_notifiers(cfg: Dict[str, Any]):
    notifiers = []
    notif_cfg = cfg.get("notifications", {})
    tg = notif_cfg.get("telegram", {})
    if tg.get("enabled"):
        notifiers.append(TelegramNotifier(token=tg["token"], chat_id=tg["chat_id"]))
    email = notif_cfg.get("email", {})
    if email.get("enabled"):
        notifiers.append(
            EmailNotifier(
                smtp_server=email["smtp_server"],
                smtp_port=email.get("smtp_port", 587),
                username=email["username"],
                password=email["password"],
                from_addr=email["from_addr"],
                to_addrs=email["to_addrs"],
            )
        )
    return notifiers

def alert(notifiers, failed_checks):
    if not failed_checks:
        return
    lines = ["*AutoNotify Alert*", "The following checks failed:"]
    for chk in failed_checks:
        lines.append(f"- `{chk['name']}` ({chk['type']})")
    message = "\n".join(lines)
    for n in notifiers:
        if isinstance(n, TelegramNotifier):
            n.send(message)
        elif isinstance(n, EmailNotifier):
            n.send(subject="AutoNotify Alert", body=message)
