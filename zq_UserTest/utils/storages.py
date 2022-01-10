import io
import os
import time
import random
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class AvatarStorage(FileSystemStorage):
    """
    头像存储
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        """
        初始化
        :param location: 保存路径
        :param base_url: 文件地址
        """
        super(AvatarStorage, self).__init__(location, base_url)

    def _open(self, name, mode='rb'):
        """
        用不到打开文件，所以省略
        """
        pass

    def content_handler(self, name, content):
        """
        处理传入数据
        :param name: 文件名
        :param content: 文件内容
        :return:
        """
        image = Image.open(content.file)

        # 标准化图片宽度
        if hasattr(settings, 'AVATAR_BASE_WIDTH') and image.width > settings.AVATAR_BASE_WIDTH:
            base_width = settings.AVATAR_BASE_WIDTH
            w_percent = base_width / float(image.size[0])
            h_size = int(float(image.size[1]) * float(w_percent))
            image = image.resize((base_width, h_size), Image.ANTIALIAS)

        # 转换格式
        new_image = io.BytesIO()
        image = image.convert('RGB')
        image.save(new_image, format='JPEG')
        new_image.seek(0)  # 返回游标到开始位置，因为后面要用到它的内容
        content.file = new_image
        content.content_type = 'image/jpeg'

        # 随机化文件名
        ext = '.jpg'  # 文件扩展名
        folder = os.path.dirname(name)  # 文件目录
        random_file_name = time.strftime('%Y%m%d%H%M%S')  # 定义文件名，年月日时分秒随机数
        random_file_name = random_file_name + '_%d' % random.randint(0, 100)
        name = os.path.join(folder, random_file_name + ext)  # 重写合成文件名

        return name, content

    def _save(self, name, content):
        """
        在本地保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS的文件名
        """
        name, content = self.content_handler(name, content)
        return super(AvatarStorage, self)._save(name, content)
