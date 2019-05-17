import json

from urllib.parse import urlencode

import tornado
from tornado import httpclient
from tornado.httpclient import HTTPRequest


class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        http_client = httpclient.AsyncHTTPClient()
        url = 'http://sms.yunpian.com/v2/sms/single_send.json'
        text = f'【fire论坛】您的验证码是{code}。如非本人操作，请忽略本短信。'
        post_requests = HTTPRequest(url=url, method='POST', body=urlencode({
            'apikey': self.api_key,
            'mobile': mobile,
            'text': text,

        }))
        res = await http_client.fetch(post_requests)
        return json.loads(res.body.decode('utf-8'))


if __name__ == '__main__':
    from functools import partial

    io_loop = tornado.ioloop.IOLoop.current()
    yun_pian = AsyncYunPian('xxx')
    args_func = partial(yun_pian.send_single_sms, '0418', '13333333333')
    io_loop.run_sync(args_func)
