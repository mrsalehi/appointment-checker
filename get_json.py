import requests
from urllib.request import urlopen, Request

# Right now it is just for Turkey embassy
def get_json(url, headers):
    req = Request(url=url, headers=headers)
    response = urlopen(req).read()

    return response.decode("utf-8")[1:-1]
