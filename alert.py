import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import datetime
import csv

delay = 3
timeStamp = []
tempList = []
userEmail = 'userEmail@gmail.com'
userNum= '+1##########'

def send_email():
    email = EmailMessage()
    email['from'] = 'Smart Aquarium Update'
    email['to'] = userEmail
    email['subject'] = 'Alert from your Smart Aquarium!'
    email.set_content('The backup-battery in your Smart-Aquarium has been enabled. This can be due to a power outage. Refer to the Smart-Aquarium website to keep an eye on the backup battery status! Note: The Smart-Aquarium will keep the aerator and filter on for as long as possible, but once the battery runs out of juice, fish can die of depleted oxygen!')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('SmartAquarium01@gmail.com', 'password')
        smtp.send_message(email)


def send_sms():
    account_sid = 'acct_sid'
    auth_token = 'acct_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='!!!The backup-battery in your Smart-Aquarium has been enabled!!!',
        from_='+1360638####',
        to= userNum
        )

def get_time():
    t = datetime.datetime.now()
    tempList.clear()
    tempList.append(int(t.year))
    tempList.append(int(t.month))
    tempList.append(int(t.day))
    tempList.append(int(t.hour))
    tempList.append(int(t.minute))
    return tempList


def new_timeStamp():
    currentTime = get_time()
    with open("timeStamp.txt", 'w') as f:
        for i in range(0,5):
             f.write(str(currentTime[i])+"\n")
    #send_email()
    #send_sms()

def send_notifications():

    currentTime = get_time()
    with open("timeStamp.txt", 'r') as f:
        readFile =  f.read()

    #alerts have sent previously
    if readFile:
        with open('timeStamp.txt', 'r') as f:
            for line in f:
                #remove newline
                number = line[:-1]
                #add item to list
                timeStamp.append(int(number))

        #print("Something exists in timeStamp file: ")
        #print("timeStamp in file: ", timeStamp)
        #print("currentTime: ", currentTime)

        #same year and month and day
        if ((currentTime[0]-timeStamp[0] or currentTime[1]-timeStamp[1] or currentTime[2]-timeStamp[2]) == 0):

            #alert sent an hour or more ago
            if currentTime[3]-timeStamp[3] > 0:
                if currentTime[3]-timeStamp[3] == 1:

                    if 60-timeStamp[4]+currentTime[4] > delay:
                        new_timeStamp()
                        #print("Change of 1 hr and diffrence in minutes > delay, sent notif and set new timestamp")

                    #else:
                        #print("Change of 1 hr but diffrence in minutes < delay, skip")

                else:
                    new_timeStamp()
                    #print("alert sent > 1 hr ago, sent notifications and set new timestamp")

            #alert not sent more than an hour ago
            else:
                #alert sent more than the delay ago
                if currentTime[4]-timeStamp[4] > delay:
                    new_timeStamp()
                    #print("alert sent more that the delay ago, sent notif and set new timestamp")

                #alert sent less than the delay ago, do nothing
                #else:
                    #print("Skip, last timeStamp < delay")


        #Not same year and same month
        else:
            new_timeStamp()
            #print("not same year, month or day, send notif and set new timeStamp")

    #No alerts sent previously
    else:
        #print("Making the first time stamp")
        new_timeStamp()



