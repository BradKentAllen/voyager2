# NEXMOmessage.py

''' Nexmo text utility
Requires keys from config.py
Message must be a string
'''

# Rev 2.0   revised Oct 9, 2020 for new nexmo sms object

import nexmo

import giblets

def sendNexmoSMS(message, phoneNumber, *args):
    '''sends SMS text using nexmo'''
    phoneList = [phoneNumber]
    if args:
        for phone in args:
            phoneList.append(phone)

    if type(message) is str:
        sms = nexmo.Sms(key=giblets.nexmoKey, secret=giblets.nexmoSecret)
        print('send message to:', end=' ')

        for phone in phoneList:
            print(phone, end=', ')
          
            sms.send_message({
                'from': giblets.nexmoPhone,
                'to': phone,
                'text': message
                })

    else:
        raise ValueError('Nexmo message must be a string')

    print('')


if __name__ == '__main__':
    print('start Nexma test')
    message = 'test message This One'
    phone_number = "4259856203"
    sendNexmoSMS(message, phone_number)
    print(f'{message} sent to {phone_number}')



