import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import RegisterSerializer, LoginTokenObtainPairSerializer

logger = logging.getLogger(__name__)


class RegisterView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        重写 post，截获异常，规范输出
        """
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            # 当出现校验失败异常时，返回首要错误信息
            for k, v in e.detail.items():
                return Response({'detail': v[0]}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'[users/register] create user {self.request.data}')  # 记录日志


class LoginTokenObtainPairView(TokenObtainPairView):
    """
    用户登录 token 获取视图
    """
    serializer_class = LoginTokenObtainPairSerializer  # 指定自定义的序列化器，校验密码

    def post(self, request, *args, **kwargs):
        logger.info(f'[users/login] get user {request.user} token')  # 记录日志
        return super().post(request, *args, **kwargs)
