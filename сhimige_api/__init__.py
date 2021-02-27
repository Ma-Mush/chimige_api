"""
Api к соцсети Chimige

Авторы:
MaMush (vk.com/maks.mushtriev2, t.me/Error_mak25, github.com/Ma-Mush)
Łukasz Tshipenchko (t.me/tshipenchko, github.com/tshipenchko)

Разработка 02.2021-н.в.
Релиз 1.0 от 27 февраля 2021 года

"""

import requests # Берегите интернет!
from json import loads
from os.path import isfile

class ChimigeError(Exception):
    pass

class Chimige():
    def __init__(self, session_name: str, email: str, password: str, force_login=False):
        """Объявление self-объекта"""
        self.req_sess = requests.Session()
        self.session_name = session_name + '.session'
        self.email = email
        self.password = password
        self.cookie = None
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Content-Length': '5',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://chimige.ru',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://chimige.ru//messages',
            'TE': 'Trailers'
            }
        if not isfile(self.session_name):
            force_login = True
        self._login(force_login)

    def _login(self, force_login=False):
        """Войти в аккаунт"""
        if force_login:
            data = {"username_email": self.email, "password": self.password}
            req = self.req_sess.post("https://chimige.ru//includes/ajax/core/signin.php",
                    headers=self.headers, data=data)
            self.cookie = "; ".join([f"{c.name}={c.value}" for c in req.cookies])
            self._save_session()
        else:
            self.cookie = self._get_session()
        self.headers["Cookie"] = self.cookie

    def _save_session(self):
        """Сохраняет сессию"""
        with open(self.session_name, "w", encoding='utf-8') as file:
            file.write(self.cookie)

    def _get_session(self):
        """Получить сессию"""
        with open(self.session_name, "r", encoding='utf-8') as file:
            return file.read()

    def msg(self, text: str, conservation_id: int or str):
        """Отправить сообщение"""
        data = {"message": text, "conversation_id": conservation_id}
        self.req_sess.post("https://chimige.ru//includes/ajax/chat/post.php", 
                headers=self.headers, data=data)
        self.req_sess.post("https://chimige.ru//includes/ajax/data/reset.php", 
                headers=self.headers, data={"reset":"messages"})

    def check_new_msg(self):
        data = {"filter":"", "last_request":0, "last_message":"0", "last_notification":0, 
                "last_post":25, "get":"newsfeed"}
        _last_message = self.req_sess.post("https://chimige.ru//includes/ajax/data/live.php",
                    data=data, headers=self.headers)
        self._last_message = _last_message
        self._last_message._content = loads(_last_message._content)
        if int(_last_message.content["conversations_count"]) >= 1:
            self._last_message.message = self._last_message._content["conversations"].split("\
                    </li><li")[0].split("class=")[1:]
            return True
        return False

    def get_new_message(self): # Да, это жестко
        class _return_message():
            pass
        message = self._last_message.message
        ret = _return_message()
        new_events = message.count('"data-content"> <div><span ')
        if len(message) >= 10 and new_events == 1:
            ret.group_chat = True
            ret.conservation_id = int(message[1].split('"')[3])
            ret.chat_name = message[1].split('"')[7]
            for i in range(3, len(message)-1):
                if message[i][1:5] == "text":
                    ret.text = message[5].split('"text">')[1].split("</div> <div")[0].split("""
                                """)[1].split("""
                        """)[0]
        elif len(message) < 9 or new_events > 1:
            ret.group_chat = False
            ret.conservation_id = int(message[1].split('"')[3])
            ret.user_id = int(message[1].split('"')[5])
            ret.user_name = message[1].split('"')[7]
            ret.user_short_name = message[1].split('"')[11]
            ret.user_photo = message[2].split('"')[3]
            ret.text = message[5].split('"text">')[1].split("</div> <div")[0].split("""
                                            """)[1].split("""
                                """)[0]
        return ret
