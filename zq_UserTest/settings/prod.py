from .base import *

# 获取环境变量
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# debug 模式
DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_HOST,  # 数据库主机
        'PORT': os.environ.get('MYSQL_PORT', 3306),  # 数据库端口
        'USER': os.environ.get('MYSQL_USER', ''),  # 数据库用户名
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),  # 数据库用户密码
        'NAME': os.environ.get('MYSQL_DATABASE', '')  # 数据库名字
    }
}

# Redis
CACHES = {
    "default": {  # 缓存数据
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}/0",
    },
    "session": {  # 缓存 session
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}/1",
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# CORS
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'https://127.0.0.1:8080',
    'https://localhost:8080',
)

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
