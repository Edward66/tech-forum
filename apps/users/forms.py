from wtforms_tornado import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Regexp, Length

MOBILE_REGEX = '^((13[0-9])|(17[0-1,6-8])|(15[^4,\\D])|(18[0-9]))\d{8}$'
PASSWORD_REGEX = '/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/'


class SmsCodeForm(Form):
    mobile = StringField('手机号码',
                         validators=[DataRequired(message='请输入手机号码'), Regexp(MOBILE_REGEX, message='请输入合法的手机号码')])


class RegisterForm(Form):
    mobile = StringField('手机号码',
                         validators=[DataRequired(message='请输入手机号码'), Regexp(MOBILE_REGEX, message='请输入合法的手机号码')])
    code = StringField('验证码', validators=[DataRequired(message='请输入验证码'), Length(min=4, max=4, message='请输入四位验证码')])
    password = StringField('密码',
                           validators=[DataRequired(message='请输入密码'), Length(min=8, max=16, message='请输入8-16位密码')])


class LoginForm(Form):
    mobile = StringField('手机号码',
                         validators=[DataRequired(message='请输入手机号码'), Regexp(MOBILE_REGEX, message='请输入合法的手机号码')])
    password = StringField('密码',
                           validators=[DataRequired(message='请输入密码'), Length(min=8, max=16, message='请输入8-16位密码')])
