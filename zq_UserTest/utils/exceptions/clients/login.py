from rest_framework import status

from zq_UserTest.utils.exceptions import ZqException


class UserNotFoundError(ZqException):
    def __init__(self):
        super(UserNotFoundError, self).__init__('A0201', '用户名不存在')


class PasswordError(ZqException):
    def __init__(self):
        super(PasswordError, self).__init__('A0201', '密码错误')


class LoginError(ZqException):
    def __init__(self):
        super(LoginError, self).__init__('A0201')
