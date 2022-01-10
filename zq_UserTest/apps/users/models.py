from django.db import models
from django.contrib.auth.models import AbstractUser

from zq_UserTest.utils.storages import AvatarStorage


class User(AbstractUser):
    """
    用户信息，扩展相关字段
    """

    avatar = models.ImageField(upload_to='avatar', default='avatar/default.jpg', verbose_name='头像',
                               storage=AvatarStorage)
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, unique=True, verbose_name='昵称')
    description = models.CharField(max_length=200, default='', verbose_name='个人简介')

    class Meta:
        app_label = 'users'
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
