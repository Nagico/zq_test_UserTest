# 自定义返回格式
from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            # 判断实例的类型，返回的数据可能是列表也可能是字典
            if isinstance(data, dict):
                # 如果是字典的话应该是返回的数据
                msg = data.pop('zq_msg', 'success')
                code = data.pop('zq_code', '00000')
            # 自定义返回数据格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
