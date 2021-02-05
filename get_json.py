import requests
import ssl
from urllib.request import urlopen, Request

# Right now it is just for Turkey embassy
def get_json(url, headers):
    req = Request(url=url, headers=headers)
    gcontext = ssl.SSLContext()
    response = urlopen(req, context=gcontext).read()
    return response.decode("utf-8")[1:-1]
