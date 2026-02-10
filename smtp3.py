import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import time

# Slow printing
def slow(text, d=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(d)
    print()

# Colors
BLUE = "\033[1;36m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"

os.system("clear" if os.name == "posix" else "cls")

# Logo
print(BLUE + r"""
      █████╗ ████████╗██╗      █████╗ ███████╗
     ██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝
     ███████║   ██║   ██║     ███████║███████╗
     ██╔══██║   ██║   ██║     ██╔══██║╚════██║
     ██║  ██║   ██║   ███████╗██║  ██║███████║
     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
""" + RESET)

# Developer link at the top
print(BLUE + "Atlas Tools - Developer: https://t.me/Atlas_2x\n" + RESET)

slow("Atlas Tools - Advanced Email Sender (Multi SMTP)", 0.04)
print("-" * 50)

# SMTP Login
smtp_email = input("Enter SMTP Email: ")
smtp_pass = input("Enter SMTP Password: ")

# Auto SMTP detection
if "@gmail.com" in smtp_email:
    smtp_server = "smtp.gmail.com"
elif "@yahoo.com" in smtp_email or "@yahoo.fr" in smtp_email:
    smtp_server = "smtp.mail.yahoo.com"
elif "@outlook.com" in smtp_email or "@hotmail.com" in smtp_email or "@live.com" in smtp_email:
    smtp_server = "smtp-mail.outlook.com"
else:
    print(RED + "Unknown email provider. Using default Gmail SMTP." + RESET)
    smtp_server = "smtp.gmail.com"

smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_email, smtp_pass)
    print(GREEN + f"\n[✓] Logged in successfully using {smtp_server}!\n" + RESET)
except Exception as e:
    print(RED + f"\n[✗] Login failed: {e}\n" + RESET)
    exit()

# Send to single or multiple emails
print(YELLOW + "Choose an option:" + RESET)
print("1) Send to a single email")
print("2) Send to multiple emails from a file")
send_choice = input(">> ")

if send_choice == "1":
    target = input("\nEnter target email: ")
elif send_choice == "2":
    file_name = input("\nEnter file name (emails.txt): ")
    if not os.path.exists(file_name):
        print(RED + "[✗] File not found." + RESET)
        exit()
    with open(file_name, "r") as f:
        emails = [x.strip() for x in f.readlines() if x.strip()]
else:
    print(RED + "Invalid choice." + RESET)
    exit()

# Message type menu
print(YELLOW + "\nChoose message type:" + RESET)
print("1) Plain Text Email")
print("2) HTML Email")
print("3) Email with File Attachment")
choice = input(">> ")

# --------------------------
# Plain Text Email
# --------------------------
if choice == "1":
    message = input("Enter your message: ")

    if send_choice == "1":
        msg = MIMEText(message)
        msg["Subject"] = "Message from Atlas Tools"
        msg["From"] = smtp_email
        msg["To"] = target
        server.sendmail(smtp_email, target, msg.as_string())
        print(GREEN + "\n[✓] Email sent!" + RESET)
    else:
        for email in emails:
            msg = MIMEText(message)
            msg["Subject"] = "Message from Atlas Tools"
            msg["From"] = smtp_email
            msg["To"] = email
            try:
                server.sendmail(smtp_email, email, msg.as_string())
                print(GREEN + f"[✓] Sent to: {email}" + RESET)
            except:
                print(RED + f"[✗] Failed to send: {email}" + RESET)

# --------------------------
# HTML Email
# --------------------------
elif choice == "2":
    print("\nWrite your HTML below:")
    print("(type ENDHTML on a new line to finish)\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "ENDHTML":
            break
        lines.append(line)
    html_content = "\n".join(lines)

    if send_choice == "1":
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "HTML Message from Atlas Tools"
        msg["From"] = smtp_email
        msg["To"] = target
        msg.attach(MIMEText(html_content, "html"))
        try:
            server.sendmail(smtp_email, target, msg.as_string())
            print(GREEN + "\n[✓] HTML Email sent!" + RESET)
        except Exception as e:
            print(RED + f"[✗] Failed to send: {e}" + RESET)
    else:
        for email in emails:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "HTML Message from Atlas Tools"
            msg["From"] = smtp_email
            msg["To"] = email
            msg.attach(MIMEText(html_content, "html"))
            try:
                server.sendmail(smtp_email, email, msg.as_string())
                print(GREEN + f"[✓] Sent to: {email}" + RESET)
            except:
                print(RED + f"[✗] Failed to send: {email}" + RESET)

# --------------------------
# Email with Attachment
# --------------------------
elif choice == "3":
    print(YELLOW + "\nChoose file type:" + RESET)
    print("1) Images (.png .jpg .jpeg)")
    print("2) Documents (.pdf .docx .txt)")
    print("3) Compressed (.zip .rar .7z)")
    print("4) Any file")
    fchoice = input(">> ")

    Tk().withdraw()
    file_path = askopenfilename(title="Choose a file to attach")
    if not file_path:
        print(RED + "[✗] No file selected." + RESET)
        exit()
    filename = os.path.basename(file_path)
    body = input("Enter your message: ")

    def send_attachment(to_email):
        msg = MIMEMultipart()
        msg["Subject"] = "File from Atlas Tools"
        msg["From"] = smtp_email
        msg["To"] = to_email
        msg.attach(MIMEText(body, "plain"))
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)
        try:
            server.sendmail(smtp_email, to_email, msg.as_string())
            print(GREEN + f"[✓] Sent to: {to_email}" + RESET)
        except:
            print(RED + f"[✗] Failed to send: {to_email}" + RESET)

    if send_choice == "1":
        send_attachment(target)
    else:
        for email in emails:
            send_attachment(email)

else:
    print(RED + "Invalid choice." + RESET)

server.quit()

