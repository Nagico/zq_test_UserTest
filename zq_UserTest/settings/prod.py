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

# Log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/zq_UserTest.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'users': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/users.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'zq_UserTest': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
        'users': {
            'handlers': ['console', 'users'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# CORS
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'https://127.0.0.1:8080',
    'https://localhost:8080',
)

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
