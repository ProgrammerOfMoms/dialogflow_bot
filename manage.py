# Импортируем созданный нами класс Server
from server import Server
# Получаем из settings.py наш api-token
from settings import token, group_id, server_name


server1 = Server(token, group_id, server_name)
# token - API токен, который мы ранее создали
# group_id - id сообщества-бота
# server_name - имя сервера

server1.start()
