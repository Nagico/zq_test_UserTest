from django.test import Client, TestCase


class RegisterTest(TestCase):
    """
    注册视图单测
    """
    def setUp(self):
        """
        初始化
        """
        self.client = Client()
        self.REGISTER_URL = '/users/register/'

    def test_get_forbidden(self):
        """
        测试 get 接口，访问被禁止访问
        :return:
        """
        response = self.client.get(self.REGISTER_URL)

        self.assertEqual(response.status_code, 405)

    def test_register_success(self):
        """
        测试注册用户
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername',
            'nickname': 'testnickname',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138000'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(type(response.json()['id']), int)
        self.assertEqual(response.json()['username'], 'testusername')
        self.assertEqual(response.json()['nickname'], 'testnickname')
        self.assertEqual(response.json()['mobile'], '13800138000')

        """
        测试注册用户，用户名已存在
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername',
            'nickname': 'testnickname',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138001'
        })

        self.assertEqual(response.status_code, 400)

        """
        测试注册用户，手机号已存在
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername2',
            'nickname': 'testnickname2',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138000'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_password_not_match(self):
        """
        测试注册用户，两次密码不匹配
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername3',
            'nickname': 'testnickname3',
            'password': 'test123456789',
            'password2': 'test12345678',
            'mobile': '13800138002'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_password_too_short(self):
        """
        测试注册用户，密码太短
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername4',
            'nickname': 'testnickname4',
            'password': '123',
            'password2': '123',
            'mobile': '13800138003'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_mobile_invalid(self):
        """
        测试注册用户，手机号格式不正确
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername5',
            'nickname': 'testnickname5',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '1380013800'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_username_too_short(self):
        """
        测试注册用户，用户名太短
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'te',
            'nickname': 'testnickname6',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138004'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_username_too_long(self):
        """
        测试注册用户，用户名太长
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername7' * 10,
            'nickname': 'testnickname7',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138005'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_nickname_too_short(self):
        """
        测试注册用户，昵称太短
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername8',
            'nickname': 'te',
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138006'
        })

        self.assertEqual(response.status_code, 400)

    def test_register_nickname_too_long(self):
        """
        测试注册用户，昵称太长
        :return:
        """
        response = self.client.post(self.REGISTER_URL, {
            'username': 'testusername9',
            'nickname': 'testnickname9' * 10,
            'password': 'test123456789',
            'password2': 'test123456789',
            'mobile': '13800138007'
        })

        self.assertEqual(response.status_code, 400)

