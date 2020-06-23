import vk_api.vk_api

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

from settings import ai_token, lang, session_id
from Bot import Bot
from db import sqlite_db
from solver import Solver

import time

class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

        # Запускаем БД
        self.db = sqlite_db

    def __get_random_id(self):
        return time.time()*1000000
    def __connect(self):
        if self.db.is_closed:
            self.db.connect()

    def send_msg(self, send_id, message, **kwargs):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message,
                                  random_id=self.__get_random_id(),
                                  **kwargs)

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(176468928, "Привет-привет!")
    
    def test_db(self):
        self.__connect()
         
    def start(self):
        try:
            self.__connect()
            solver = Solver()
            for event in self.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    payload = event.object.payload
                    if payload == None:
                        payload = False
                    if not payload:
                        #get dialogflow bot instanse
                        bot = Bot(ai_token, lang, session_id)
                        #get text, resolved intent and msg params 
                        text, intent, params, action = bot.send_msg(event.object.text)
                        #processing 
                        resolve, p = solver.run(intent, params, event.object.peer_id)
                        # print(f"Интент: {intent}")
                        if resolve:
                            self.send_msg(event.object.peer_id, resolve, **p)
                            if action:
                                resolve, p = solver.action_solver(action, event.object.peer_id)
                                if resolve and p:
                                    self.send_msg(event.object.peer_id, resolve, **p)

                        else: 
                            prefix = solver.set_prefix(intent, params)
                            postfix = solver.set_postfix(intent, params)
                            text = f'{prefix}{text}{postfix}' 
                            self.send_msg(event.object.peer_id, text)
                            if action:
                                resolve, p = solver.action_solver(action, event.object.peer_id)
                                if resolve and p:
                                    self.send_msg(event.object.peer_id, resolve, **p)
                    else:
                        resolve, p = solver.resolve_payload(payload, event.object.peer_id)
                        self.send_msg(event.object.peer_id, resolve, **p)
        except:
            if not self.db.is_closed:
                self.db.close()
            exit()
