import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client
import logging
import datetime
import pytz
from time import sleep

logging.basicConfig(filename='logs.out', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
my_number = os.environ['MY_NUMBER']
sis_number = os.environ['SIS_NUMBER']
# bro_number = os.environ['BRO_NUMBER']
twilio_number = os.environ['TWILIO_NUMBER']

client = Client(account_sid, auth_token)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
url = "https://ais.usvisa-info.com/en-ir/ir_availability"

logging.info("The code is up and running!")

while True:
    try:
        pacific = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(pacific).strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Checking at: {now}.")
        response = requests.get(url, headers=headers)
        html_string = response.content.decode()
        soup = BeautifulSoup(html_string, 'html.parser')

        # print(soup.prettify())

        # DUBAI
        link = soup.find("a", href="/en-ae/niv")
        dubai_tag = link.parent.find_next_sibling()
        for child in dubai_tag.children:
            if "All Other Visa Types:" in child.text:
                if "There are no available appointments at this time." in child.text:
                    text = child.text.replace("All Other Visa Types: ", "")
                    text = "Dubai:" + text + " " + now
                    logging.info(text)
                    my_message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=my_number
                    )
                    logging.info(my_message.sid)
                    # sis_message = client.messages.create(
                    #     body=text,
                    #     from_=twilio_number,
                    #     to=sis_number
                    # )
                    # logging.info(sis_message.sid)
                    # bro_message = client.messages.create(
                    #     body=text,
                    #     from_=twilio_number,
                    #     to=bro_number
                    # )
                    # logging.info(bro_message.sid)

        # YEREVAN
        link = soup.find("a", href="/en-am/niv")
        yerevan_tag = link.parent.find_next_sibling()
        for child in yerevan_tag.children:
            if "All Other Visa Types:" in child.text:
                if "There are no available appointments at this time." not in child.text:
                    text = child.text.replace("All Other Visa Types: ", "")
                    text = "Yerevan: " + text + " " + now
                    logging.info(text)
                    my_message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=my_number
                    )
                    logging.info(my_message.sid)
                    sis_message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=sis_number
                    )
                    logging.info(sis_message.sid)
                    # bro_message = client.messages.create(
                    #     body=text,
                    #     from_=twilio_number,
                    #     to=bro_number
                    # )
                    # logging.info(bro_message.sid)
                    
        # ANKARA
        link = soup.find("a", href="/en-tr/niv")
        ankara_tag = link.parent.find_next_sibling()
        for child in ankara_tag.children:
            if "All Other Visa Types:" in child.text:
                if "There are no available appointments at this time." not in child.text:
                    text = child.text.replace("All Other Visa Types: ", "")
                    text = child.text.replace("All Other Visa Types: ", "")
                    text = "Ankara: " + text + " " + now
                    logging.info(text)
                    my_message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=my_number
                    )
                    logging.info(my_message.sid)
                    sis_message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=sis_number
                    )
                    logging.info(sis_message.sid)
                    # bro_message = client.messages.create(
                    #     body=text,
                    #     from_=twilio_number,
                    #     to=bro_number
                    # )
                    # logging.info(bro_message.sid)
        sleep(30)
    except Exception as e:
        logging.error(e)
        sleep(30)