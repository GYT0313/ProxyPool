import requests

PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            print(response.text)
            return response.text
    except ConnectionError:
        return None


def get_httpbin(proxy):
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print(e.args)


if __name__ == '__main__':
    proxy = get_proxy()
    get_httpbin(proxy)