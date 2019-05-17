import json
import requests

web_url = 'http://127.0.0.1:8001'


def test_sms():
    url = f"{web_url}/code/"
    data = {
        'mobile': '13888888888',
    }
    res = requests.post(url, json=data)
    print(json.loads(res.text))


def test_register():
    url = f"{web_url}/register/"
    data = {
        'mobile': '13888888888',
        'code': '1231',
        'password': '112233aa',
    }
    res = requests.post(url, json=data)
    print(json.loads(res.text))


if __name__ == '__main__':
    # test_sms()
    test_register()
