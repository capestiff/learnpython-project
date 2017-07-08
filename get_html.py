import requests

def get_html(url, params=None):
    user_agent = {'User-agent': 'Mozilla/5.0'}

    try:
        result = requests.get(url=url, headers=user_agent, params=params)

        result.raise_for_status()

        if result.status_code == requests.codes.ok:
            return result.text
        else:
            print('Can\'t get html by url.')
    except requests.RequestException as error:
        print(error)
        return '<html><head></head><body><table><tr><td></td></tr></table></body></html>'
