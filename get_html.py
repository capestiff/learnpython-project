import requests

def get_html(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    result = requests.get(url=url, headers=user_agent)
    if result.status_code == requests.codes.ok:
        return result.text
    else:
        print('Can\'t get html by url.')
