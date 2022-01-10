from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status as drf_status

# 获取在配置文件中定义的logger，用来记录日志
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger('django')

DEFAULT_MSG = {
        '00000': ('success', drf_status.HTTP_200_OK),
        'A0001': '用户端错误',
        'A0100': '用户注册错误',
        'A0110': '用户名校验失败',
        'A0111': '用户名已存在',
        'A0112': '用户名包含敏感词',
        'A0113': '用户名包含特殊字符',
        'A0120': '密码校验失败',
        'A0121': '密码长度不够',
        'A0122': '密码强度不够',
        'A0130': '验证码输入错误',
        'A0131': '短信验证码输入错误',
        'A0132': '邮件验证码输入错误',
        'A0133': '验证码过期',
        'A0140': '用户基本信息校验失败',
        'A0141': '学号格式校验失败',
        'A0142': '邮箱格式校验失败',
        'A0143': '学院格式校验失败',
        'A0200': ('用户账户登录异常', drf_status.HTTP_401_UNAUTHORIZED),
        'A0201': ('用户名或密码错误', drf_status.HTTP_401_UNAUTHORIZED),
        'A0202': ('用户账户被冻结', drf_status.HTTP_401_UNAUTHORIZED),
        'A0203': ('用户账户已作废', drf_status.HTTP_401_UNAUTHORIZED),
        'A0204': ('用户输入密码次数超限', drf_status.HTTP_401_UNAUTHORIZED),
        'A0205': ('用户登录信息异常', drf_status.HTTP_401_UNAUTHORIZED),
        'A0206': ('用户登录凭证生成失败', drf_status.HTTP_401_UNAUTHORIZED),
        'A0207': ('用户未注册', drf_status.HTTP_401_UNAUTHORIZED),
        'A0210': ('用户第三方登录失败', drf_status.HTTP_401_UNAUTHORIZED),
        'A0211': ('用户第三方账户被冻结', drf_status.HTTP_401_UNAUTHORIZED),
        'A0212': ('用户第三方账户名或密码错误', drf_status.HTTP_401_UNAUTHORIZED),
        'A0213': ('用户第三方登录验证码错误', drf_status.HTTP_401_UNAUTHORIZED),
        'A0214': ('用户未提供第三方登录验证码', drf_status.HTTP_401_UNAUTHORIZED),
        'A0215': ('用户第三方登录已过期', drf_status.HTTP_401_UNAUTHORIZED),
        'A0220': ('用户登录已过期', drf_status.HTTP_401_UNAUTHORIZED),
        'A0300': ('用户访问权限异常', drf_status.HTTP_401_UNAUTHORIZED),
        'A0301': ('未提供访问此功能所需的登录信息', drf_status.HTTP_401_UNAUTHORIZED),
        'A0310': ('用户访问被拦截', drf_status.HTTP_403_FORBIDDEN),
        'A0311': ('用户账号被冻结',drf_status.HTTP_403_FORBIDDEN),
        'A0312': ('不在服务时段',drf_status.HTTP_403_FORBIDDEN),
        'A0400': '用户请求参数错误',
        'A0401': '请求 JSON 解析失败',
        'A0402': '请求必填参数为空',
        'A0410': '请求参数值错误',
        'A0411': '参数格式不匹配',
        'A0412': '参数超出允许的取值范围',
        'A0420': '用户输入内容非法',
        'A0421': '输入字数过多',
        'A0422': '包含违禁敏感词',
        'A0423': '图片包含违禁信息',
        'A0430': '用户操作异常',
        'A0500': '用户请求服务异常',
        'A0501': '请求次数超出限制',
        'A0502': '请求并发数超出限制',
        'A0503': '操作排队请等待',
        'A0504': 'WebSocket 连接异常',
        'A0505': 'WebSocket 连接断开',
        'A0506': '用户重复请求',
        'A0507': '请求合法性校验失败',
        'A0508': ('请求的接口不存在', drf_status.HTTP_404_NOT_FOUND),
        'A0600': '用户资源异常',
        'A0601': '用户配额已用光',
        'A0700': '用户上传文件异常',
        'A0701': '用户上传文件类型不匹配',
        'A0702': '用户上传文件太大',
        'A0703': '用户上传文件太小',
        'A0800': '用户请求版本异常',
        'A0801': '用户 API 请求版本不匹配',
        'A0802': '用户 API 请求版本过高',
        'A0803': '用户 API 请求版本过低',
        'A1000': '用户设备异常',
        'A1100': '用户信息接口错误',
    }


def get_zq_exception_response(code, msg=None, status=None):
    """
    获取自强错误信息
    :param code: 错误码
    :param msg: 错误信息(可选)
    :param status: http 状态码(可选)
    :return: Response
    """
    if not msg or not status:
        # 获取默认信息
        default = DEFAULT_MSG.get(code, code)

        if type(default) == str:
            default_msg = default
            default_status = drf_status.HTTP_400_BAD_REQUEST
        else:
            default_msg = default[0]
            default_status = default[1]

        if not msg:
            msg = default_msg
        if not status:
            status = default_status
    
    return Response({
        'zq_code': code,
        'zq_msg': msg,
    }, status=status)


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    if isinstance(exc, ZqException):
        # zq 定义异常
        return get_zq_exception_response(exc.code, exc.msg)

    if isinstance(exc, NotAuthenticated):
        # 未登录
        return get_zq_exception_response('A0301')

    if isinstance(exc, InvalidToken):
        # token错误
        return get_zq_exception_response('A0205')

    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']

        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=drf_status.HTTP_507_INSUFFICIENT_STORAGE)

    return response


class ZqException(Exception):
    """
    zq 异常类
    """
    def __init__(self, code, msg=None, status=None):
        self.code = code
        self.msg = msg
        self.status = status
