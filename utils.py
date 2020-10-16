def parse_cookies(cookie_string):
    cookies = cookie_string.split(';')
    
    cookie_list = []
    for pair in cookies:
        name = pair.split('=')[0].strip()
        value = pair.split('=')[1].strip()
        cookie_list.append({'name': name, 'value': value})
    
    return cookie_list
    