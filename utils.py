def parse_cookies(cookie_string):
    cookies = cookie_string.split(';')
    
    cookie_list = []
    for pair in cookies:
        name = pair.split('=')[0].strip()
        value = pair.split('=')[1].strip()
        cookie_list.append({'name': name, 'value': value})
    
    return cookie_list

def cookies_list_to_string(cookies_list):
    cookies_string = '; '.join([f"{pair['name']}={pair['value']}" for pair in cookies_list])
    return cookies_string
