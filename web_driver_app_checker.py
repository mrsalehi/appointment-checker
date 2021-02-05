from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import logging
import argparse
import yaml
from get_json import get_json
from utils import cookies_list_to_string
from datetime import date
import calendar
import ssl
from send_email import send_email

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# parser = argparse.ArgumentParser()
# parser.add_argument("--embassy", type=str, default="turkey")
# parser.add_argument("--re", action="store_true")
# parser.add_argument("--verbose", action="store_true")

# 'dubai': "https://ais.usvisa-info.com/en-ae/niv/users/sign_in",
# 'cyprus': "https://ais.usvisa-info.com/en-cy/niv/users/sign_in",
# 'cyprus': 'https://ais.usvisa-info.com/en-cy/niv/schedule/31274313/appointment/days/117.json?appointments[expedite]=false',

LOG_IN_URLS = {
    'turkey': "https://ais.usvisa-info.com/en-tr/niv/users/sign_in",
    'armenia': "https://ais.usvisa-info.com/en-am/niv/users/sign_in",    
    'toronto': "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
}

AVAILABLE_APPS_URLS = {
    'turkey': 'https://ais.usvisa-info.com/en-tr/niv/schedule/30816904/appointment/days/124.json?appointments[expedite]=false',
    'armenia': 'https://ais.usvisa-info.com/en-am/niv/schedule/31148073/appointment/days/122.json?appointments[expedite]=false',
    'toronto': 'https://ais.usvisa-info.com/en-ca/niv/schedule/32555879/appointment/days/94.json?appointments[expedite]=false'
}


def find_app_dates(app_str):
    keyword = '{"date":"'

    dates = []

    while keyword in app_str:
        pos = app_str.find(keyword)
        date = app_str[pos+9:pos+19]
        year, month, date = [int(x) for x in date.split('-')]
        app_str = app_str[pos+20:]
        dates.append((year, month, date))

    return dates


def main(args, driver, credentials):
    try:
        driver.get(LOG_IN_URLS[args['embassy']])

        driver.find_element_by_id("user_email").send_keys(credentials[args['embassy']]['user'])
        driver.find_element_by_id("user_password").send_keys(credentials[args['embassy']]['pass'])
        driver.find_element_by_class_name("icheck-area-20").click()
        window_before = driver.window_handles[0]

        driver.find_element_by_name("commit").click()
        time.sleep(2)
        driver.find_element_by_link_text('Continue').click()
        time.sleep(2)
        
        if not args['re']:
            driver.find_element_by_link_text("Schedule Appointment").click()
            time.sleep(2)
            driver.find_elements_by_link_text("Schedule Appointment")[1].click()
        else:
            resc_app = driver.find_elements_by_class_name("accordion-title")[3]
            resc_app.click()
            time.sleep(2)
            driver.find_elements_by_link_text("Reschedule Appointment")[1].click()
        
        apps_str = get_json(AVAILABLE_APPS_URLS[args['embassy']], headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 
            'Cookie': cookies_list_to_string(driver.get_cookies())
            })

        # if not apps_str:
        #     if args.verbose:
        #         logging.info('No appointments available.')

        if apps_str:
            if args['embassy'] == 'toronto':
                dates = find_app_dates(apps_str)
                april_apps = [el for el in dates if el[1] == 4]

                if april_apps:
                    day = april_apps[0][2]
                    send_email(f'{day} April!')
            
            elif args['embassy'] != 'cyprus':
                dates = find_app_dates(apps_str)
                if dates:
                    day = dates[0][2]
                    month = calendar.month_name[dates[0][1]]
                    year = dates[0][0]
                    send_email(f'{day} {month} {year}')

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        # driver.close()


if __name__ == '__main__':
    with open('/Users/mrezasalehi/Desktop/personal-projects/appointment-checker/credentials.yml') as file:
        credentials = yaml.load(file, Loader=yaml.FullLoader)
    driver = webdriver.Firefox(log_path='/tmp/geckodriver.log')
    driver.minimize_window()
    main({'embassy': 'toronto', 're': True}, driver, credentials)
    main({'embassy': 'armenia', 're': False}, driver, credentials)
    main({'embassy': 'turkey', 're': False}, driver, credentials)
    driver.close()