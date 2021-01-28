import asyncio
import json
import logging
import websockets


class WebSocketUtility:
    __instance = None
    __should_send = False
    __message = None
    Users = set()
    WebSocketDict = {}

    @staticmethod
    def get_instance():
        if WebSocketUtility.__instance == None:
            WebSocketUtility()
        return WebSocketUtility.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if WebSocketUtility.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            WebSocketUtility.__instance = self

    def set_send_status(self, flag):
        self.__should_send = flag

    def get_send_status(self):
        return self.__should_send

    def set_stock_list(self, msg):
        self.__message = msg

    def get_stock_list(self):
        return self.__message
