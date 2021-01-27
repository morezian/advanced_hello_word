import asyncio
import json
import logging
import websockets

class WebSocketUtility:
    __instance = None
    #__users = None
    __should_send = False
    __message = None
    Users = set()
    
    @staticmethod
    def getInstance():
        if WebSocketUtility.__instance == None:
            WebSocketUtility()
        return WebSocketUtility.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if WebSocketUtility.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            WebSocketUtility.__instance = self
            #self.__users = set()
            #start_server = websockets.serve(self.notify_all, "localhost", 6789)
            #asyncio.get_event_loop().run_until_complete(start_server)
            #asyncio.get_event_loop().run_forever()

    async def notify_all(self, websocket, path):
        #self.register(websocket)
        while True:
            if self.__should_send == True:
                await websocket.send(self.get_stock_list())
                self.__should_send = False
    
    def set_send_status(self, flag):
        self.__should_send = flag
    
    def set_stock_list(self, msg):
        self.__message = msg
        
    def get_stock_list(self):
        return self.__message
        
"""s = Singleton()
print s

s = Singleton.getInstance()
print s

s = Singleton.getInstance()
print s"""
