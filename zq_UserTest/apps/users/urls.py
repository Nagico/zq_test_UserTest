from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = routers.SimpleRouter()

urlpatterns = [
    # 登陆注册
    path('register/', views.RegisterView.as_view(), name='token_obtain_pair'),  # 注册
    path('login/', views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新token

    # 登录用户详细信息
    path('', views.UserDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user_detail'),
]

