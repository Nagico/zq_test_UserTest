"""zq_UserTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import CurrentTimeViewSet
from zq_UserTest.utils.views import APIRootViewSet

urlpatterns = [
    path('users/', include('users.urls'), name='users'),  # 用户
    path('time/', CurrentTimeViewSet.as_view({  # 本用户anime收藏
        'get': 'list'
    }), name='time'),
    path('api_schema/', SpectacularAPIView.as_view(), name='schema'),  # API 文档
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # swagger接口文档
    path('', APIRootViewSet.as_view({'get': 'list'}), name='root'),
]

# 添加静态文件路径 仅 DEBUG 可以使用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
