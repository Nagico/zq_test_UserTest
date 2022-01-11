import datetime
import logging
import random
from time import sleep

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import RegisterSerializer, LoginTokenObtainPairSerializer, UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = RegisterSerializer

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


class UserDetailViewSet(RetrieveModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin,
                        GenericViewSet):
    """
    该用户信息视图
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # 仅登录用户可访问个人信息

    def get_object(self):
        """
        重写对象获取逻辑，获取当前登录用户的信息
        """
        obj = self.get_queryset().list()  # 从jwt鉴权中获取当前登录用户的uid
        if obj is None:
            raise NotFound('用户不存在', code='user_not_found')
        return obj

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'[users/] get private user {request.user} info')  # 记录日志
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        支持部分更新
        """
        kwargs['partial'] = True
        logger.info(f'[users/] update private user {request.user} info: {request.data}')  # 记录日志
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
        logger.info(f'[users/] delete private user {self.request.user} info')  # 记录日志


class CurrentTimeViewSet(GenericViewSet):
    def list(self, request):
        sleep_time = random.random() * 2 + 2
        sleep(sleep_time)
        return Response({'current_time': datetime.datetime.now()}, status=status.HTTP_200_OK)
