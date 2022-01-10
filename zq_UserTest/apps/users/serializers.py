import re

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
import zq_UserTest.utils.exceptions.clients.register as register_exceptions
import zq_UserTest.utils.exceptions.clients.login as login_exceptions


class RegisterSerializer(serializers.ModelSerializer):
    """
    注册序列化器
    """

    # 序列化器的所有字段 ['id', 'username', 'nickname', 'password', 'password2', 'mobile']
    # 校验字段 ['username', 'nickname', 'password', 'password2', 'mobile']
    # 已存在字段 ['id', 'username', 'nickname', 'password', 'mobile']

    # 需要序列化（后端响应）的字段 ['id', 'username', 'mobile', 'access', 'refresh']
    # 需要反序列化（前端传入）的字段 ['username', 'nickname', 'password', 'password2', 'mobile']  write_only=True

    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False)
    mobile = serializers.CharField(label='手机号', help_text='手机号', required=True, allow_blank=False)
    password = PasswordField(label='密码', write_only=True)
    password2 = PasswordField(label='确认密码', write_only=True)
    refresh = serializers.CharField(label='刷新令牌', read_only=True)  # JWT
    access = serializers.CharField(label='访问令牌', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'password', 'password2', 'mobile', 'refresh', 'access']  # 序列化器内容

    def validate_username(self, value):
        """
        用户名校验
        """
        if not re.match(r'^[a-zA-Z0-9_]{6,16}$', value):
            raise register_exceptions.UsernameValidationError

        if User.objects.filter(username=value).exists():
            raise register_exceptions.UsernameAlreadyExistsError

        return value

    def validate_nickname(self, value):
        """
        昵称校验
        """
        if not re.match(r'^[a-zA-Z0-9_]{6,16}$', value):
            raise register_exceptions.RegisterValidationError('昵称格式错误')

        return value

    def validate_mobile(self, value):
        """
        手机号校验
        """
        if not re.match(r'1[3-9]\d{9}', value):
            raise register_exceptions.RegisterValidationError('手机号格式错误')
        if User.objects.filter(mobile=value).exists():
            raise register_exceptions.RegisterValidationError('手机号已存在')

        return value

    def validate_password(self, value):
        """
        密码校验
        """
        if not re.match(r'^[A-Za-z\d.,/;:"\'\[\]\\<>|()\-=+`~@$!%*#?&]{8,24}$', value):
            raise register_exceptions.PasswordValidationError

        return value

    def validate(self, attrs):
        """
        校验密码
        """
        # 判断两次密码是否一致
        if attrs['password'] != attrs['password2']:
            raise register_exceptions.PasswordUniformityError

        return attrs

    @staticmethod
    def get_tokens_for_user(user):
        """
        生成用户 token
        :param user: 用户对象
        :return: token 字典
        """
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        """
        创建用户, 追加返回 jwt token
        """
        # 删除数据库中不需要的字段
        del validated_data['password2']

        password = validated_data.pop('password')  # 避免密码明文存储

        # 创建用户
        user = User(**validated_data)
        user.set_password(password)  # 密码加密
        user.save()

        # 生成jwt token
        token = self.get_tokens_for_user(user)
        user.refresh = token['refresh']
        user.access = token['access']

        return user


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    登录获取token序列化器
    """

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed as e:
            raise login_exceptions.LoginError

        refresh = self.get_token(self.user)

        data['id'] = self.user.id
        data['username'] = self.user.username
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器（所有信息）
    """
    class Meta:
        model = User
        exclude = ['is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login',
                   'first_name', 'last_name', 'groups', 'user_permissions', 'email']
        read_only_fields = ['username', 'mobile']

    password = PasswordField(write_only=True)
    password2 = PasswordField(write_only=True)

    def validate_avatar(self, value):
        """
        头像检测
        """
        if not value:  # 未找到头像文件
            return settings.DEFAULT_AVATAR_PATH

        if value.content_type not in ['image/jpeg', 'image/png', 'image/gif']:  # 文件类型不正确
            raise register_exceptions.FileTypeError

        if value.size > 1024 * 1024 * 2:  # 头像文件大于2M
            raise register_exceptions.FileTooLargeError
        if value.size < 1024:  # 头像文件小于1KB
            raise register_exceptions.FileTooSmallError

        if self.instance.avatar != settings.DEFAULT_AVATAR_PATH:  # 已存在头像文件
            self.instance.avatar.delete()  # 删除原头像文件

        return value

    def validate_nickname(self, value):
        """
        昵称校验
        """
        if not re.match(r'^[a-zA-Z0-9_]{6,16}$', value):
            raise register_exceptions.RegisterValidationError('昵称格式错误')

        return value

    def validate_password(self, value):
        """
        密码校验
        """
        if not value:
            return value
        if not re.match(r'^[A-Za-z\d.,/;:"\'\[\]\\<>|()\-=+`~@$!%*#?&]{8,24}$', value):
            raise register_exceptions.PasswordValidationError

        return value

    def validate(self, attrs):
        """
        联合校验密码
        :param attrs:
        :return:
        """
        if 'password' in attrs and 'password2' in attrs:
            # rsa 解密
            password = attrs['password']
            password2 = attrs['password2']

            if password != password2:
                raise register_exceptions.PasswordUniformityError

            attrs['password'] = make_password(password)
            attrs.pop('password2')  # 删除密码2

        return attrs
