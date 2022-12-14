# Twilio_SMS.py

''' Twilio SMS text send utility
API key stored in giblets.py
Message must be a string
'''

# Rev 1.0  created Feb 8, 2022 using NEXMO as template
# rev 1.1  Nov 2022, add date, new Twilio info

import datetime

from twilio.rest import Client

# Twilio auth is in giblets
import giblets

def send_SMS_message(message, phone_number, *args):
    '''sends SMS text using nexmo'''
    client = Client(giblets.twilio_API_sid, giblets.twilio_API_token)

    phoneList = [phone_number]
    if args:
        for phone in args:
            phoneList.append(phone)

    if type(message) is str:
        
        print('send message to:', end=' ')

        for phone in phoneList:
            print(phone, end=', ')
            message = client.messages.create(
                to=phone_number, 
                from_= giblets.twilio_phone_number,
                body=message)

    else:
        raise ValueError('Twilio message must be a string')

    print('')


if __name__ == '__main__':
    print('start Twilio test')
    #message = 'test message This One'
    date_string = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    message = f'Twilio test at {date_string}'

    phone_number = "+14259856203"
    send_SMS_message(message, phone_number)
    #print(f'{message} sent to {phone_number}')



