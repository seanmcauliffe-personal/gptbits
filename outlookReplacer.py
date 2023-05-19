import win32com.client
import os
import datetime
import re

def initialize_outlook():
    return win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

def clean_subject(subject):
    return re.sub(r'[\/:*?"<>|]', '', subject)

def create_directory(base_dir):
    today = datetime.date.today()
    year_dir = os.path.join(base_dir, str(today.year))
    month_dir = os.path.join(year_dir, str(today.month))
    day_dir = os.path.join(month_dir, str(today.day))
    os.makedirs(day_dir, exist_ok=True)
    return day_dir

def get_messages(outlook):
    inbox = outlook.GetDefaultFolder(6)
    return inbox.Items

def save_message(message, day_dir):
    sender = message.SenderEmailAddress
    subject = message.Subject
    body = message.Body
    timestamp = message.ReceivedTime
    email_content = f"Sender: {sender}\nSubject: {subject}\nReceived: {timestamp}\n\n{body}"
    clean_subj = clean_subject(subject)
    with open(os.path.join(day_dir, f"{clean_subj}.txt"), "w", encoding="utf-8") as file:
        file.write(email_content)

def filter_messages(messages, sender_filter, day_dir):
    message = messages.GetFirst()
    while message:
        if message.SenderEmailAddress == sender_filter:
            save_message(message, day_dir)
        message = messages.GetNext()

def send_email(outlook, recipient, subject, body):
    mail = outlook.CreateItem(0)
    mail.Recipients.Add(recipient)
    mail.Subject = subject
    mail.Body = body
    mail.Send()

def main():
    outlook = initialize_outlook()
    base_dir = os.path.join(os.getcwd(), "email_directory")
    day_dir = create_directory(base_dir)
    messages = get_messages(outlook)
    filter_messages(messages, "sender@example.com", day_dir)
    send_email(outlook, "recipient@example.com", "Test Subject", "This is a test email.")

if __name__ == "__main__":
    main()
