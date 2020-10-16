from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import logging
import argparse
import yaml
import ghasedak
from get_json import get_json
from utils import cookies_list_to_string
from datetime import date
import calendar

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
SMS = ghasedak.Ghasedak('5c4fe5bf481fc9882613f70b003b6319e54a76a76a1114924f72b2440920685d')

parser = argparse.ArgumentParser()
parser.add_argument("--embassy", type=str, default="turkey")
parser.add_argument("--re", action="store_true")


LOG_IN_URLS = {
    'turkey': "https://ais.usvisa-info.com/en-tr/niv/users/sign_in",
    'armenia': "https://ais.usvisa-info.com/en-am/niv/users/sign_in",    
    'cyprus': "https://ais.usvisa-info.com/en-cy/niv/users/sign_in",
    'dubai': "https://ais.usvisa-info.com/en-ae/niv/users/sign_in"
}

AVAILABLE_APPS_URLS = {
    'turkey': 'https://ais.usvisa-info.com/en-tr/niv/schedule/30816904/appointment/days/124.json?appointments[expedite]=false',
    'armenia': 'https://ais.usvisa-info.com/en-am/niv/schedule/31148073/appointment/days/122.json?appointments[expedite]=false',
    'cyprus': 'https://ais.usvisa-info.com/en-cy/niv/schedule/31274313/appointment/days/117.json?appointments[expedite]=false'
}


def launch_driver(args, credentials):
    driver = webdriver.Firefox()
    driver.get(LOG_IN_URLS[args.embassy])

    driver.find_element_by_id("user_email").send_keys(credentials[args.embassy]['user'])
    driver.find_element_by_id("user_password").send_keys(credentials[args.embassy]['pass'])
    driver.find_element_by_class_name("icheck-area-20").click()
    window_before = driver.window_handles[0]

    driver.find_element_by_name("commit").click()
    time.sleep(10)
    driver.find_element_by_link_text('Continue').click()
    time.sleep(10)
    if not args.re:
        driver.find_element_by_link_text("Schedule Appointment").click()
        time.sleep(2)
        driver.find_elements_by_link_text("Schedule Appointment")[1].click()
    else:
        resc_app = driver.find_elements_by_class_name("accordion-title")[3]
        resc_app.click()
        time.sleep(2)
        driver.find_elements_by_link_text("Reschedule Appointment")[1].click()

    while True:
        time.sleep(10)

        apps_str = get_json(AVAILABLE_APPS_URLS[args.embassy], headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 
            'Cookie': cookies_list_to_string(driver.get_cookies())
            })

        if not apps_str:
            logging.info('No appointments available.')
        else:
            tmp_str = apps_str[:apps_str.find('}')]
            year, month, date = [int(x) for x in tmp_str[9:19].split('-')]
            SMS.send({
                'message': f'{args.embassy}: {date} {calendar.month_name[month]}, {year}', 
                'receptor' : '09029279793', 
                'linenumber': '5000121212'})
            exit(0)
        
        driver.refresh()



if __name__ == '__main__':
    parser.parse_args()
    args = parser.parse_args()
    with open('credentials.yml') as file:
        credentials = yaml.load(file, Loader=yaml.FullLoader)
    
    launch_driver(args, credentials)