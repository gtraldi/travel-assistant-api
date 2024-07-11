import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_addrs, body):
    from_addr = "jt5v7lekovzrxsvp@ethereal.email"
    login = "jt5v7lekovzrxsvp@ethereal.email"
    password = "AFEzkUBqhUMUvQx8Um"

    msg = MIMEMultipart()
    msg["form"] = "travels_confirm@email.com"
    msg["to"] = ", ".join(to_addrs)

    msg["Subject"] = "Travel Confirmation!"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP("smtp.ethereal.email", 587)
    server.starttls()
    server.login(login, password)
    text = msg.as_string()

    for email in to_addrs:
        server.sendmail(from_addr, email, text)

    server.quit()