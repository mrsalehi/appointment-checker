from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import logging
import argparse
import yaml
import ghasedak

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
SMS = ghasedak.Ghasedak('5c4fe5bf481fc9882613f70b003b6319e54a76a76a1114924f72b2440920685d')

parser = argparse.ArgumentParser()
parser.add_argument("--embassy", type=str, default="turkey")
parser.add_argument("--re", action="store_true")


URLS = {
    'turkey': "https://ais.usvisa-info.com/en-tr/niv/users/sign_in",
    'armenia': "https://ais.usvisa-info.com/en-am/niv/users/sign_in",    
    'cyprus': "https://ais.usvisa-info.com/en-cy/niv/users/sign_in",
    'dubai': "https://ais.usvisa-info.com/en-ae/niv/users/sign_in"
}


def launch_driver(args, credentials):
    driver = webdriver.Firefox()
    driver.get(URLS[args.embassy])

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
        time.sleep(30)
        if 'There are no available appointments at the selected location. Please try again later.' in driver.find_element_by_tag_name("body").text:
            logging.info('No appointments available.')
        else:
            SMS.send({
                'message': f'Appointment available at {args.embassy} embassy!', 
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