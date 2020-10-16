import sys
import requests
import requests, lxml.html
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
import logging
import ghasedak


SMS = ghasedak.Ghasedak('5c4fe5bf481fc9882613f70b003b6319e54a76a76a1114924f72b2440920685d')
COOKIE = '_ga=GA1.2.899588692.1586876789; _gid=GA1.2.1220338506.1600695222; _gat=1; _yatri_session=STdKNitJTGgwclRSZVB1T2hidXcwTU1lNlQ4dzVDTGVDVUF2VEhFR3FkNU5GRnhjMytTQlZvK0RaQVNBNnRIOUludmtkRWtwbjJGcFRnem1qR3JMRStHTzR2ZDJydjZkakU4UUduSTZBWlhJdG5IMlBoZUFzYlRpQi83a0lHUk93T0FDZnJoSzNHNnhlcGRJbjNxSmpmM1JGQkZYN2NJbGhOdUNOVmlDdVk2RVAvVGN5OXJ1TTlMTkZGVHgxMisrQUJBMm5QRnpLa1FIQndWQ1N1TXFWQ3A0UzF1SjlhWno3OWpldElELzN0b3NOdFd1WWJwSE9JVlVjSThOejFZREdZWWZ0bWlPUDNDRHhubExJOVhTbzRqRnhyOWdhaEVuN2ZSb2FBZ3hORElGMllyOGhjOHI0RytFWmV6YldSWFUzczU4T0Mva1BBZ3lUVTBsY3dWNFhENThxcm1sRklWN0pvR29LOFZYd3pDTlJ0U0hkV1FLNHpoZTUwbXh4Ti9oQ053dU1XNS9JVnBRTWhRU1lxTmo2ckJaMVZrR1g1aTRpcTlraUZaTFhEczZXOUlJVXREOWcyK0xNVHNBdC9WaU1IamkrNHEyQk5oQkx4U1ZoNGZiWDNjRDlTaTFyNUt1M1M0akwzRmQ3aEU9LS16K1Y2M2dxQ2VCZGlYbDk1NXJ3VnNBPT0%3D--7c52bfbbe619fd7e857c9aaf94a176afcf00d2fc'
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def appointment_checker(url: str, embassy: str):
    while True:
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 
        'Referer': 'https://ais.usvisa-info.com/en-tr/niv/schedule/30816904/appointment',
        'Cookie': COOKIE
        }
        req = Request(url=url, headers=headers)
        response = urlopen(req).read()
        html_string = response.decode('utf-8')
        soup = BeautifulSoup(html_string, 'lxml')
        if 'There are no available appointments at the selected location. Please try again later' in soup.text:
            logging.info(f'No Appointments available at {embassy} embassy.')
        else:
            SMS.send({'message': f'Appointment available at {embassy} embassy!', 
            'receptor' : '09029279793', 
            'linenumber': '5000121212'})
            exit(0)

        time.sleep(30)
        

if __name__ == "__main__":
    url = "https://ais.usvisa-info.com/en-tr/niv/schedule/30816904/appointment"
    embassy = 'Turkey'
    appointment_checker(url, embassy)
