from rest_framework import status

from zq_UserTest.utils.exceptions import ZqException
from zq_UserTest.utils.exceptions.clients.file import *


class RegisterValidationError(ZqException):
    """
    通用的注册格式错误
    """
    def __init__(self, message):
        super().__init__('A0140', message, status=status.HTTP_400_BAD_REQUEST)


class UsernameAlreadyExistsError(ZqException):
    """
    用户名已存在
    """
    def __init__(self):
        super().__init__('A0111')


class UsernameValidationError(ZqException):
    """
    用户名格式错误
    """
    def __init__(self):
        super().__init__('A0110')


class PasswordValidationError(ZqException):
    """
    密码格式错误
    """
    def __init__(self):
        super().__init__('A0120', '密码格式错误')


class PasswordUniformityError(ZqException):
    """
    密码一致性校验错误
    """
    def __init__(self):
        super().__init__('A0121', '密码不一致')
