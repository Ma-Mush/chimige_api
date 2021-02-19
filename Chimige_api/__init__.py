"""
Api к соцсети Chimige

Авторы:
MaMush (vk.com/maks.mushtriev2, t.me/Error_mak25, github.com/Ma-Mush)
Łukasz Tshipenchko (t.me/tshipenchko, github.com/tshipenchko)

Разработка 02.2021-н.в.
"""

import requests
import pickle
import os.path

class ChimigeError(Exception):
    pass

class Chimige(object):
    def __init__(self, session_name: str, email: str, password: str):
        """Объявление self-объекта"""
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

    def _not_exited(self):
        if self.cookie == "exited":
            raise ChimigeError("Вы уже вышли!")
        else:
            return True

    def _save_session(self):
        """Сохраняет сессию"""
        with open(self.session_name, "wb") as f:
            pickle.dump(self.cookie, f)

    def _get_session(self):
        """Получить сессию"""
        with open(self.session_name, "rb") as f:
            return pickle.load(f)

    def _is_exist_session(self):
        """Проверяет, есть ли сессия"""
        return os.path.isfile(self.session_name)

    def login(self, force_login=False):
        """Войти в аккаунт"""
        if not self._is_exist_session() or force_login:
            data = {"username_email": self.email, "password": self.password}
            r = requests.post("https://chimige.ru//includes/ajax/core/signin.php",
                              headers=self.headers, data=data)
            self.cookie = "; ".join([f"{c.name}={c.value}" for c in r.cookies])
        else:
            self.cookie = self._get_session()
        self.headers["Cookie"] = self.cookie

    def sess_exit(self, force_sing_out=False):
        """Выходит из аккаунта"""
        if force_sing_out:  
            pass
        else:
            self._save_session()
            self.cookie = "exited"
            self.headers = "exited"

    def msg(self, text: str, conservation_id: int or str):
        """Отправить сообщение"""
        if self._not_exited():
            data = {"message": text, "conversation_id": conservation_id}
            r = requests.post("https://chimige.ru//includes/ajax/chat/post.php", headers=self.headers, data=data)
            return r.text

