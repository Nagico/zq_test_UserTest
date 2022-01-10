from rest_framework import status

from zq_UserTest.utils.exceptions import ZqException


class FileValidationError(ZqException):
    """
    通用的文件校验错误
    """
    def __init__(self, message):
        super().__init__('A0700', message, status=status.HTTP_400_BAD_REQUEST)


class FileTypeError(FileValidationError):
    """
    文件类型错误
    """
    def __init__(self):
        super().__init__('A0701')


class FileTooLargeError(ZqException):
    """
    文件太大
    """
    def __init__(self):
        super().__init__('A0702')


class FileTooSmallError(ZqException):
    """
    文件太小
    """
    def __init__(self):
        super().__init__('A0703')
