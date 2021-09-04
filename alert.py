import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import os

def send_email():
    email = EmailMessage()
    email['from'] = 'Smart Aquarium Update'
    email['to'] = 'SmartAquarium01@gmail.com'
    email['subject'] = 'Alert from your Smart Aquarium!'
    email.set_content('The backup-battery in your Smart-Aquarium has been enabled. This can be due to a power outage. Refer to the Smart-Aquarium website to keep an eye on the backup battery status! Note: The Smart-Aquarium will keep the aerator and filter on for as long as possible, but once the battery runs out of juice, fish can die of depleted oxygen!')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('SmartAquarium01@gmail.com', 'STank99!')
        smtp.send_message(email)
        print('Email has been sent!')


def send_sms():
    account_sid = os.environ['ACb9e945b53cb9b665d913e472830312bc']
    auth_token = os.environ['5ce0a24779accc15b7db717e9209f7e5']
    
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(
        to="+19568907076",
        from_="+13606383914",
        body="The backup-battery in your Smart-Aquarium has been enabled")
    print("SMS has been sent")