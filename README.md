# сhimige_api

## Импорт 

Для начала - импортируем класс Chimige для работы с апи - from chimige_api import Chimige

## Вход - Chimige(session_name: str, email: str, password: str, force_login=False)

Войти в аккаунт Чимиге можно вызвав класс Chimige и записать вернувшиеся данные в переменную, например
```python
session = Chimige("Имя сессии", "email или короткое имя", "пароль")
```

Название | Описание
--------|---------
session_name | Название сессии для записи ее в файл
email | email аккаунта или его короткий адрес
password | Пароль
force_login | Это что за покемон? А, ВСПОМНИЛ, если сессия уже есть в файле, то все равно войти заново (True) или использовать записанную (False)


## Отправка сообщения - _.msg(text: str, conservation_id: int or str)

Отправить сообщение можно вызвав функцию msg, например 
```python
session.msg("Привет Лукасу от детей России!", "ид диалога с неким Лукасом")
```
Название | Описание
--------|---------
text | текст
converчего.. conservation_id | ид диалога с пользователем (ДА, НЕ ЮЗЕР ИД! :((( )

## Проверка наличия новых сообщений - _.check_new_msg()

Проверить наличие новых сообщений можно вызвав функцию check_new_msg, например
```python
if session.check_new_msg(): ...
```
Воришка, не воруй! (параметры)

## Получение последнего нового сообщения - get_new_message()

ИСПОЛЬЗОВАТЬ ТОЛЬКО ПОСЛЕ check_new_msg 

Получить последнее новое сообщение можно испольпользвовав функцию get_new_message, например
```python
if session.check_new_msg(): 
    event = get_new_message()
```
Возвращает self-объект (использование - event.text, например)
Название | Описание
--------|---------
group_chat | True (если сообщение из группового чата)/False (если из ЛС)
text | текст
conservation_id | ид диалога с пользователем
user_id (если group_chat == False) | id пользователя 
user_name (если group_chat == False) | ФИ пользователя
user_short_name (если group_chat == False) | Короткое имя пользователя 
chat_name (если group_chat == True) | Название чата

Помоги Даше найти параметры...

# Примеры кода

```python
from chimige_api import Chimige
ch = Chimige("Ses", "cool_email@cool.cool", "mega_password")
while True:
    if ch.check_new_msg():
        mess = ch.get_new_message()
        txt = mess.text.lower().split()
        con_id = mess.conservation_id
        if txt[0] == "эй," and len(txt) == 2:
            ch.msg(f"Я тебе не {txt[1]}", con_id)
```
