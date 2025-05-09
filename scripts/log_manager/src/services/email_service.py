import json
import smtplib
import configparser

# Configuration parser
config = configparser.ConfigParser()
# Read the configuration file
inconfig.read("./res/watchdog.conf")
email = config['email']['sender']
key = config['email']['key']

subject = input("SUBJECT: ")
message = input("MESSAGE: ")

with open("../../data/email_adresses.json", "r") as f:
    receivers = json.loads(f.read())

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, key)

# Send email to all receivers
for receiver in receivers:
    server.sendmail(email, receiver['email'], text)

server.quit()
print("Email sent successfully!")