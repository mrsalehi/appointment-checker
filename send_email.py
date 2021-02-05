import smtplib

SENDER_USER = 'msreza76@gmail.com'
SENDER_PASSWORD = 'Salehi76primarypassword'
RCVR_USER = 'mrezasal1@gmail.com'

EMAIL_TEMPLATE = """\
From: %s
To: %s
Subject: %s

%s
"""

def send_email(body):
    global EMAIL_TEMPLATE
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(SENDER_USER, SENDER_PASSWORD)
        server.sendmail(SENDER_USER, RCVR_USER, EMAIL_TEMPLATE % (
            SENDER_USER, 
            RCVR_USER, 
            'Appointment Available in April!', 
            body))
        server.close()
    except:
        print('Something went wrong.... Could not send the email!')
