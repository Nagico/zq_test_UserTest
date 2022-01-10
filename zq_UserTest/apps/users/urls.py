from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()

urlpatterns = [
    # 登陆注册
    path('register/', views.RegisterView.as_view(), name='token_obtain_pair'),  # 注册
]

