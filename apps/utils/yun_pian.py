import requests


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_single_sms(self, code, mobile):
        """发送单条短信"""
        url = 'https://sms.yunpian.com/v2/sms/single_send.json'
        text = f'【fire论坛】the1fire论坛，您的验证码是{code}。如非本人操作，请忽略本短信。'
        res = requests.post(url, data={
            'apikey': self.api_key,
            'mobile': mobile,
            'text': text
        })
        return res


# 测试的时候把白名单ip关闭掉，上线的时候开启然后将云服务器的固定ip加进去
if __name__ == '__main__':
    yun_pian = YunPian('xxx')
    res = yun_pian.send_single_sms('0418', '13888888888')
    print(res.text)
