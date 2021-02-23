"""
Api к соцсети Chimige

Авторы:
MaMush (vk.com/maks.mushtriev2, t.me/Error_mak25, github.com/Ma-Mush)
Łukasz Tshipenchko (t.me/tshipenchko, github.com/tshipenchko)

Разработка 02.2021-н.в.
"""

import requests
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
        self.password = str(password)
        self.cookie = None
        self.headers = {'Content-type': 'application/x-www-form-urlencoded',
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
            r = self.req_sess.post("https://chimige.ru//includes/ajax/core/signin.php",
                              headers=self.headers, data=data)
            self.cookie = "; ".join([f"{c.name}={c.value}" for c in r.cookies])
            self._save_session()
        else:
            self.cookie = self._get_session()
        self.headers["Cookie"] = self.cookie

    def _save_session(self):
        """Сохраняет сессию"""
        with open(self.session_name, "w", encoding='utf-8') as f:
            f.write(self.cookie)

    def _get_session(self):
        """Получить сессию"""
        with open(self.session_name, "r", encoding='utf-8') as f:
            return f.read()

    def msg(self, text: str, conservation_id: int or str):
        """Отправить сообщение"""
        data = {"message": text, "conversation_id": conservation_id}
        self.req_sess.post("https://chimige.ru//includes/ajax/chat/post.php", 
                      headers=self.headers, data=data)
        self.req_sess.post("https://chimige.ru//includes/ajax/data/reset.php", 
                      headers=self.headers, data={"reset":"messages"})

# Пока не работает
# И не будет
# а как жить
    # def send_photo(self, path, conservation_id, message=None):


    def check_new_msg(self):
        data = {"filter":"", "last_request":0, "last_message":"0", "last_notification":0, 
                "last_post":25, "get":"newsfeed"}
        _last_message = self.req_sess.post("https://chimige.ru//includes/ajax/data/live.php",
                          data=data, headers=self.headers)
        self._last_message = _last_message
        self._last_message._content = loads(_last_message._content)
        if int(_last_message.content["conversations_count"]) >= 1:
            self._last_message.message = self._last_message._content["conversations"].split("</li><li")[0].split("class=")[1:]
            return True
        return False

    def get_new_message(self):
        class _ret_message():
            pass
        message = self._last_message.message
        if len(message) >= 10:
            group_chat = True
            conservation_id = int(message[1].split('"')[3])
            chat_name = message[1].split('"')[7]
            for i in range(3, len(message)-1):
                if message[i][1:5] == "text":
                    text = message[5].split('"text">')[1].split("</div> <div")[0].split("""
                                """)[1].split("""
                        """)[0]
            ret = _ret_message()
            ret.group_chat = group_chat
            ret.conservation_id = conservation_id
            ret.text = text
            ret.chat_name = chat_name
            return ret
        elif len(message) == 7:
            group_chat = False
            conservation_id = int(message[1].split('"')[3])
            user_id = int(message[1].split('"')[5])
            user_name = message[1].split('"')[7]
            user_short_name = message[1].split('"')[11]
            user_photo = message[2].split('"')[3]
            text = message[5].split('"text">')[1].split("</div> <div")[0].split("""
                                            """)[1].split("""
                                """)[0]
            ret = _ret_message()
            ret.group_chat = group_chat
            ret.conservation_id = conservation_id
            ret.text = text
            ret.user_id = user_id
            ret.user_name = user_name
            ret.user_short_name = user_short_name
            ret.user_photo = user_photo
            return ret
        return message
