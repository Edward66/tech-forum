import json
from datetime import datetime
from random import choice

import jwt

from tornado.web import RequestHandler

from apps.users.forms import SmsCodeForm, RegisterForm, LoginForm
from apps.utils.async_yun_pian import AsyncYunPian
from apps.users.models import User
from tech_forum.hanlder import RedisHandler


class SmsHandler(RedisHandler):
    def generate_code(self):
        """
        生成随机4位数字的验证码
        :return:
        """
        numbers = '0123456789'
        random_str = []
        for i in range(4):
            random_str.append(choice(numbers))
        return ''.join(random_str)

    async def post(self, *args, **kwargs):
        return_data = {}

        params = self.request.body.decode('utf-8')
        params = json.loads(params)
        # tornado并不会帮我们处理json数据，所以从用户那取到的是字符串。form在传递进来的时候会默认取第一个值，所以只能取到第一个字母。
        # wtforms_json可以解决这个问题
        sms_form = SmsCodeForm.from_json(params)  # wtforms_json用猴子补丁实现的
        if sms_form.validate():
            mobile = sms_form.mobile.data
            code = self.generate_code()
            yun_pian = AsyncYunPian('x')
            return_json = await yun_pian.send_single_sms(code, mobile)
            if return_json["code"] != 0:
                self.set_status(400)
                return_data["mobile"] = return_json["msg"]
            else:
                # 将验证码写入到redis中
                self.redis_conn.set(f'{mobile}_{code}', 1, 10 * 60)  # 值为1，代表code存在，10分钟过期
        else:
            self.set_status(400)  # 参数错误
            for field in sms_form.errors:
                return_data[field] = sms_form.errors[field][0]
        self.finish(return_data)


class RegisterHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        return_data = {}
        params = self.request.body.decode('utf-8')
        params = json.loads(params)
        register_form = RegisterForm.from_json(params)  # wtforms_json用猴子补丁实现的
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 验证码是否正确
            redis_key = f'{mobile}_{code}'  # redis查询的是内存非常快，所以没有必要去使用异步的redis。后期可以用aioredis实现一下异步的redis
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                return_data['code'] = '验证码错误或者失效'
            else:
                # 验证用户是否存在
                try:
                    existed_users = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    return_data['code'] = '用户已存在'
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    return_data['id'] = user.id
        else:
            self.set_status(400)
            for field in register_form.erros:
                return_data[field] = register_form[field][0]
        self.finish(return_data)


class LoginHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        return_data = {}
        params = self.request.body.decode('utf-8')
        params = json.loads(params)
        login_form = LoginForm.from_json(params)
        if login_form.validate():
            mobile = login_form.mobile.data
            password = login_form.password.data

            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password):  # check_password将明文的密码加密成密文
                    self.set_status(400)
                    return_data['non_fields'] = '用户名或密码错误'
                else:
                    # 登录成功,jwt本质是加密技术
                    # 生成json web token
                    payload = {
                        'id': user.id,
                        'nickname': user.nickname,
                        'exp': datetime.utcnow(),  # jwt内部过期用到的也是utcnow
                    }
                    token = jwt.encode(payload, self.settings['secret_key'], algorithm='HS256')
                    return_data['id'] = user.id
                    if user.nickname is not None:
                        return_data['nickname'] = user.nickname
                    else:
                        return_data['nickname'] = user.mobile
                    return_data['token'] = token.decode('utf-8')
            except User.DoesNotExist as e:
                self.set_status(400)
                return_data['mobile'] = '用户不存在'
        self.finish(return_data)
